from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Integer, UniqueConstraint, and_, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.users.models import User


class Textbook(Base):
    name: Mapped[str] = mapped_column(index=True, unique=True)
    slug: Mapped[Optional[str]] = mapped_column(
        unique=False,
        index=True,
        nullable=True,
    )
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="textbook",
    )
    users: Mapped[list["User"]] = relationship(
        back_populates="textbooks",
        secondary="usertextbook",
    )

    def __repr__(self):
        return self.name


class Lesson(Base):
    name: Mapped[str] = mapped_column(index=True)
    slug: Mapped[Optional[str]] = mapped_column(
        unique=False,
        index=True,
        nullable=True,
    )
    textbook_id: Mapped[int] = mapped_column(
        ForeignKey("textbook.id", ondelete="CASCADE")
    )
    __table_args__ = (UniqueConstraint("name", "textbook_id"),)

    textbook: Mapped["Textbook"] = relationship(
        back_populates="lessons",
    )
    users: Mapped[Optional[list["User"]]] = relationship(
        back_populates="lessons",
        secondary="userlesson",
    )

    def __repr__(self):
        return self.name


class UserTextbook(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    textbook_id: Mapped[int] = mapped_column(
        ForeignKey("textbook.id", ondelete="CASCADE"),
        nullable=False,
    )
    completed: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default=text("false"),
    )
    __table_args__ = (UniqueConstraint("user_id", "textbook_id"),)

    user: Mapped["User"] = relationship(viewonly=True)
    textbook: Mapped["Textbook"] = relationship(viewonly=True)

    userlessons: Mapped[Optional[list["UserLesson"]]] = relationship(
        back_populates="usertextbook",
    )

    def __repr__(self):
        return f"{self.user}: {self.textbook}"


class UserLesson(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lesson.id", ondelete="CASCADE"),
        nullable=False,
    )
    # TODO: возможно нужно убрать, так как обхожусь сырым SQL
    usertextbook_id: Mapped[int] = mapped_column(
        ForeignKey("usertextbook.id", ondelete="CASCADE"),
        nullable=False,
    )
    # TODO: server-default - не работает
    completed: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default=text("false"),
    )
    __table_args__ = (UniqueConstraint("user_id", "lesson_id"),)

    user: Mapped["User"] = relationship(viewonly=True)
    lesson: Mapped["Lesson"] = relationship(viewonly=True)
    usertextbook: Mapped["UserTextbook"] = relationship(
        back_populates="userlessons",
    )
    classes: Mapped[Optional[list["Class"]]] = relationship(
        secondary="classuserlesson",
        back_populates="userlessons",
    )

    def __repr__(self):
        return f"{self.user}: {self.lesson}"
