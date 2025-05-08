import enum
from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    JSON,
    CheckConstraint,
    Date,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.textbooks.models import UserLesson


class EntityType(enum.Enum):
    GRAMMAR = "grammar"
    TOPIC = "topic"


class UsefulLink(Base):
    url: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)

    entity_type: Mapped[EntityType] = mapped_column(
        Enum(EntityType),
        nullable=False,
    )  # only "grammar" or "topic"
    grammar_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("grammar.id", ondelete="CASCADE"),
        nullable=True,
    )
    topic_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("topic.id", ondelete="CASCADE"),
        nullable=True,
    )
    __table_args__ = (
        CheckConstraint(
            "(grammar_id IS NOT NULL AND topic_id IS NULL) OR (grammar_id IS NULL AND topic_id IS NOT NULL)",
            name="check_only_one_entity_type",
        ),
    )
    grammar: Mapped[Optional["Grammar"]] = relationship(
        "Grammar",
        back_populates="useful_links",
        foreign_keys=[grammar_id],
    )
    topic: Mapped[Optional["Topic"]] = relationship(
        "Topic",
        back_populates="useful_links",
        foreign_keys=[topic_id],
    )

    def __repr__(self):
        return f"{self.id}: {self.url[:15]}"


class Word(Base):
    kanji: Mapped[Optional[str]] = mapped_column(nullable=True)
    kana: Mapped[str] = mapped_column(nullable=False)
    translation: Mapped[Optional[str]] = mapped_column(nullable=True)
    example_sentences: Mapped[Optional[str]] = mapped_column(nullable=True)
    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lesson.id", ondelete="CASCADE"),
        nullable=True,
    )

    __table_args__ = (UniqueConstraint("kana", "translation"),)

    classes: Mapped[Optional[list["Class"]]] = relationship(
        secondary="classword",
        back_populates="words",
    )

    def __repr__(self):
        if self.kana and not self.kanji:
            return self.kana
        elif self.kana and self.kanji:
            return f"{self.kanji}: ({self.kana})"


class Grammar(Base):
    name_russian: Mapped[str] = mapped_column(index=True, unique=True)
    name_japanese: Mapped[Optional[str]] = mapped_column(nullable=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson.id", ondelete="CASCADE"))

    useful_links: Mapped[Optional[list[UsefulLink]]] = relationship(
        "UsefulLink",
        back_populates="grammar",
    )
    classes: Mapped[Optional[list["Class"]]] = relationship(
        secondary="classgrammar",
        back_populates="grammar_topics",
    )

    def __repr__(self):
        return self.name_russian


class Topic(Base):
    name_russian: Mapped[str] = mapped_column(index=True, unique=True)
    name_japanese: Mapped[Optional[str]] = mapped_column(nullable=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson.id", ondelete="CASCADE"))

    useful_links: Mapped[Optional[list[UsefulLink]]] = relationship(
        "UsefulLink",
        back_populates="topic",
    )
    classes: Mapped[Optional[list["Class"]]] = relationship(
        secondary="classtopic",
        back_populates="other_topics",
    )

    def __repr__(self):
        return self.name_russian
