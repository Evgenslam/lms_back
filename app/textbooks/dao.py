from app.services import CRUDBase
from app.textbooks.models import Lesson, Textbook, UserLesson, UserTextbook


class CRUDTextbook(CRUDBase):

    model = Textbook


class CRUDLesson(CRUDBase):

    model = Lesson


class CRUDUserTextbook(CRUDBase):

    model = UserTextbook


class CRUDUserLesson(CRUDBase):

    model = UserLesson
