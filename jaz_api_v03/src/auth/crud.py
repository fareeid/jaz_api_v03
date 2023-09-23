from src.auth.models import User
from src.auth.schemas import UserCreate, UserUpdate
from src.db.crud_base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):  # type: ignore
    pass
