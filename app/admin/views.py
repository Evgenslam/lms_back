from sqladmin import ModelView

from app.textbooks.models import Lesson, Textbook, UserLesson
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.email]
    column_list += [User.textbooks]
    column_list += [User.lessons]
    column_details_exclude_list = [User.hashed_password]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class TextbookAdmin(ModelView, model=Textbook):
    column_list = [c.name for c in Textbook.__table__.columns]
    column_list += [Textbook.lessons]
    column_list += [Textbook.users]
    form_create_rules = ["name", "slug"]
    name = "Учебник"
    name_plural = "Учебники"
    icon = "fa-solid fa-book"


class LessonAdmin(ModelView, model=Lesson):
    column_list = [c.name for c in Lesson.__table__.columns]
    column_list += [Lesson.textbook]
    column_list += [Lesson.users]
    form_create_rules = ["name", "textbook", "users"]
    name = "Урок"
    name_plural = "Уроки"
    icon = "fa-solid fa-glasses"


class UserLessonAdmin(ModelView, model=UserLesson):
    column_list = [UserLesson.user, UserLesson.lesson, UserLesson.completed]
    form_create_rules = ["user", "lesson", "completed"]
    name = "Урок пользователя"
    name_plural = "Уроки пользователя"
    icon = "fa-solid fa-pencil"
