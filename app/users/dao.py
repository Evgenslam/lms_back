from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import IncorrectEmailOrPasswordException
from app.services import CRUDBase
from app.users.models import User


class CRUDUser(CRUDBase):

    model = User
