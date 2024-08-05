from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    name: Mapped[str] = mapped_column(String(128))
    username: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    phone: Mapped[str] = mapped_column(nullable=True)
    nic: Mapped[str] = mapped_column(nullable=True)
    pin: Mapped[str] = mapped_column(nullable=True)
    lic_no: Mapped[str] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(nullable=True)
    dob: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    cust_code: Mapped[str] = mapped_column(String(10), nullable=True)
    cust_cc_code: Mapped[str] = mapped_column(nullable=True)
    cust_customer_type: Mapped[str] = mapped_column(nullable=True)
    user_flexi: Mapped[str] = mapped_column(JSONB, nullable=True)
    premia_cust_payload: Mapped[str] = mapped_column(JSONB, nullable=True)
    agency_admin: Mapped[bool] = mapped_column(server_default="false")
    is_staff: Mapped[bool] = mapped_column(server_default="false")
    staff_admin: Mapped[bool] = mapped_column(server_default="false")
    is_active: Mapped[bool] = mapped_column(server_default="false")
    is_superuser: Mapped[bool] = mapped_column(server_default="false")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"  # noqa: E501
