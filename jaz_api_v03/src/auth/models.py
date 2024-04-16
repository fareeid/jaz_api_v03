from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)
    nic: Mapped[str] = mapped_column(nullable=True)
    pin: Mapped[str] = mapped_column(nullable=True)
    agent_code: Mapped[str] = mapped_column(String(10), nullable=True)
    agency_admin: Mapped[bool] = mapped_column(server_default="false")
    is_staff: Mapped[bool] = mapped_column(server_default="false")
    staff_admin: Mapped[bool] = mapped_column(server_default="false")
    is_active: Mapped[bool] = mapped_column(server_default="false")
    is_superuser: Mapped[bool] = mapped_column(server_default="false")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"  # noqa: E501
