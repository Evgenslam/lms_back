from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.classes.models import Class
    from app.textbooks.models import Lesson, Textbook


# TODO: research viewonly
class User(Base):
    name: Mapped[str] = mapped_column(unique=False)
    slug: Mapped[Optional[str]] = mapped_column(
        unique=False,
        nullable=True,
    )
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(nullable=True)

    textbooks: Mapped[Optional[list["Textbook"]]] = relationship(
        back_populates="users",
        secondary="usertextbook",
    )
    lessons: Mapped[Optional[list["Lesson"]]] = relationship(
        back_populates="users",
        secondary="userlesson",
    )
    lessons_completed: Mapped[Optional[list["Lesson"]]] = relationship(
        back_populates="users",
        secondary="userlesson",
        primaryjoin="and_(UserLesson.user_id == User.id, UserLesson.completed == True)",
        viewonly=True,  # Ensures SQLAlchemy doesn't try to modify this
    )
    classes: Mapped[Optional[list["Class"]]] = relationship(
        back_populates="user",
    )

    def __repr__(self):
        return f"пользователь с почтой {self.email}"
