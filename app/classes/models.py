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


class Class(Base):
    class_date: Mapped[date] = mapped_column(Date, index=True)  # Дата или дата-время
    name: Mapped[str] = mapped_column(index=True)
    slug: Mapped[Optional[str]] = mapped_column(
        unique=False,
        index=True,
        nullable=True,
    )
    # TODO: нужно ли выделять plan и homework в отдельные таблицы, чтобы сделать уроки в них кликабельными?
    plan: Mapped[Optional[str]] = mapped_column(nullable=True)
    homework: Mapped[Optional[str]] = mapped_column(nullable=True)
    questions: Mapped[Optional[str]] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
    )
    __table_args__ = (UniqueConstraint("class_date", "user_id"),)
    user: Mapped["User"] = relationship(
        back_populates="classes",
    )
    userlessons: Mapped[Optional[list["UserLesson"]]] = relationship(
        secondary="classuserlesson",
        back_populates="classes",
    )
    words: Mapped[Optional[list["Word"]]] = relationship(
        secondary="classword",
        back_populates="classes",
    )
    grammar_topics: Mapped[Optional[list["Grammar"]]] = relationship(
        secondary="classgrammar",
        back_populates="classes",
    )
    other_topics: Mapped[Optional[list["Topic"]]] = relationship(
        secondary="classtopic",
        back_populates="classes",
    )

    def __repr__(self):
        return self.name


class ClassWord(Base):
    class_id: Mapped[int] = mapped_column(
        ForeignKey("class.id", ondelete="CASCADE"),
        nullable=False,
    )
    word_id: Mapped[int] = mapped_column(
        ForeignKey("word.id", ondelete="CASCADE"),
        nullable=False,
    )
    __table_args__ = (UniqueConstraint("class_id", "word_id"),)

    def __repr__(self):
        return f"{self.class_id}: {self.word_id}"


class ClassGrammar(Base):
    class_id: Mapped[int] = mapped_column(
        ForeignKey("class.id", ondelete="CASCADE"),
        nullable=False,
    )
    grammar_id: Mapped[int] = mapped_column(
        ForeignKey("grammar.id", ondelete="CASCADE"),
        nullable=False,
    )
    __table_args__ = (UniqueConstraint("class_id", "grammar_id"),)

    def __repr__(self):
        return f"{self.class_id}: {self.grammar_id}"


class ClassTopic(Base):
    class_id: Mapped[int] = mapped_column(
        ForeignKey("class.id", ondelete="CASCADE"),
        nullable=False,
    )
    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topic.id", ondelete="CASCADE"),
        nullable=False,
    )
    __table_args__ = (UniqueConstraint("class_id", "topic_id"),)

    def __repr__(self):
        return f"{self.class_id}: {self.topic_id}"


class ClassUserLesson(Base):
    class_id: Mapped[int] = mapped_column(
        ForeignKey("class.id", ondelete="CASCADE"),
        nullable=False,
    )
    userlesson_id: Mapped[int] = mapped_column(
        ForeignKey("userlesson.id", ondelete="CASCADE"),
        nullable=False,
    )
    __table_args__ = (UniqueConstraint("class_id", "userlesson_id"),)

    def __repr__(self):
        return f"{self.class_id}: {self.userlesson_id}"
