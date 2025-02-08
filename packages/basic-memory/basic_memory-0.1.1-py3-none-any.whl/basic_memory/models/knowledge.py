"""Knowledge graph models."""

import re
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Integer,
    String,
    Text,
    ForeignKey,
    UniqueConstraint,
    DateTime,
    Index,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from basic_memory.models.base import Base
from enum import Enum

from basic_memory.utils import generate_permalink


class Entity(Base):
    """
    Core entity in the knowledge graph.

    Entities represent semantic nodes maintained by the AI layer. Each entity:
    - Has a unique numeric ID (database-generated)
    - Maps to a file on disk
    - Maintains a checksum for change detection
    - Tracks both source file and semantic properties
    """

    __tablename__ = "entity"
    __table_args__ = (
        UniqueConstraint("permalink", name="uix_entity_permalink"),  # Make permalink unique
        Index("ix_entity_type", "entity_type"),
        Index("ix_entity_title", "title"),
        Index("ix_entity_created_at", "created_at"),  # For timeline queries
        Index("ix_entity_updated_at", "updated_at"),  # For timeline queries
    )

    # Core identity
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    entity_type: Mapped[str] = mapped_column(String)
    entity_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    content_type: Mapped[str] = mapped_column(String)

    # Normalized path for URIs
    permalink: Mapped[str] = mapped_column(String, unique=True, index=True)
    # Actual filesystem relative path
    file_path: Mapped[str] = mapped_column(String, unique=True, index=True)
    # checksum of file
    checksum: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Metadata and tracking
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)

    # Relationships
    observations = relationship(
        "Observation", back_populates="entity", cascade="all, delete-orphan"
    )
    outgoing_relations = relationship(
        "Relation",
        back_populates="from_entity",
        foreign_keys="[Relation.from_id]",
        cascade="all, delete-orphan",
    )
    incoming_relations = relationship(
        "Relation",
        back_populates="to_entity",
        foreign_keys="[Relation.to_id]",
        cascade="all, delete-orphan",
    )

    @property
    def relations(self):
        return self.incoming_relations + self.outgoing_relations

    @validates("permalink")
    def validate_permalink(self, key, value):
        """Validate permalink format.

        Requirements:
        1. Must be valid URI path component
        2. Only lowercase letters, numbers, and hyphens (no underscores)
        3. Path segments separated by forward slashes
        4. No leading/trailing hyphens in segments
        """
        if not value:
            raise ValueError("Permalink must not be None")

        if not re.match(r"^[a-z0-9][a-z0-9\-/]*[a-z0-9]$", value):
            raise ValueError(
                f"Invalid permalink format: {value}. "
                "Use only lowercase letters, numbers, and hyphens."
            )
        return value

    def __repr__(self) -> str:
        return f"Entity(id={self.id}, name='{self.title}', type='{self.entity_type}'"


class ObservationCategory(str, Enum):
    TECH = "tech"
    DESIGN = "design"
    FEATURE = "feature"
    NOTE = "note"
    ISSUE = "issue"
    TODO = "todo"


class Observation(Base):
    """
    An observation about an entity.

    Observations are atomic facts or notes about an entity.
    """

    __tablename__ = "observation"
    __table_args__ = (
        Index("ix_observation_entity_id", "entity_id"),  # Add FK index
        Index("ix_observation_category", "category"),  # Add category index
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_id: Mapped[int] = mapped_column(Integer, ForeignKey("entity.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=ObservationCategory.NOTE.value,
        server_default=ObservationCategory.NOTE.value,
    )
    context: Mapped[str] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[list[str]]] = mapped_column(
        JSON, nullable=True, default=list, server_default="[]"
    )

    # Relationships
    entity = relationship("Entity", back_populates="observations")

    @property
    def permalink(self) -> str:
        """
        Create synthetic permalink for the observation
            We can construct these because observations are always
            defined in and owned by a single entity
        """
        return generate_permalink(
            f"{self.entity.permalink}/observations/{self.category}/{self.content}"
        )

    def __repr__(self) -> str:
        return f"Observation(id={self.id}, entity_id={self.entity_id}, content='{self.content}')"


class Relation(Base):
    """
    A directed relation between two entities.
    """

    __tablename__ = "relation"
    __table_args__ = (
        UniqueConstraint("from_id", "to_id", "relation_type", name="uix_relation"),
        Index("ix_relation_type", "relation_type"),
        Index("ix_relation_from_id", "from_id"),  # Add FK indexes
        Index("ix_relation_to_id", "to_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_id: Mapped[int] = mapped_column(Integer, ForeignKey("entity.id", ondelete="CASCADE"))
    to_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("entity.id", ondelete="CASCADE"), nullable=True
    )
    to_name: Mapped[str] = mapped_column(String)
    relation_type: Mapped[str] = mapped_column(String)
    context: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationships
    from_entity = relationship(
        "Entity", foreign_keys=[from_id], back_populates="outgoing_relations"
    )
    to_entity = relationship("Entity", foreign_keys=[to_id], back_populates="incoming_relations")

    @property
    def permalink(self) -> str:
        """Create relation permalink showing the semantic connection:
        source/relation_type/target
        e.g., "specs/search/implements/features/search-ui"
        """

        return generate_permalink(
            f"{self.from_entity.permalink}/{self.relation_type}/{self.to_entity.permalink}"
            if self.to_entity
            else f"{self.from_entity.permalink}/{self.relation_type}/{self.to_name}"
        )

    def __repr__(self) -> str:
        return f"Relation(id={self.id}, from_id={self.from_id}, to_id={self.to_id}, to_name={self.to_name}, type='{self.relation_type}')"
