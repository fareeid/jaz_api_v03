from ..db.crud_base import BaseCRUD
from .models import Item
from .schemas import ItemCreate, ItemUpdate


class CRUDItem(BaseCRUD[Item, ItemCreate, ItemUpdate]):
    """Item actions with basic CRUD operations"""

    pass


item = CRUDItem(Item)
