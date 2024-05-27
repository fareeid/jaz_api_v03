from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from ...db.base import Base


class Payload(Base):
    pl_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pl_data: Mapped[str] = mapped_column(index=True)
    payload: Mapped[str] = mapped_column(JSONB, nullable=True)
