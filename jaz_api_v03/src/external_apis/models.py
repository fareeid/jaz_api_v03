from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base


class ExternalPayload(Base):
    ep_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    external_party: Mapped[str] = mapped_column(index=True)
    transaction_type: Mapped[str] = mapped_column(index=True)
    notification: Mapped[str] = mapped_column(index=True)
    payload: Mapped[str] = mapped_column(JSONB, nullable=True)
