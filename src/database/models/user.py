from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Users(BigIntAuditBase):
    __tablename__ = "users"
    name: Mapped[str]  = mapped_column(String(50), nullable=False)
    surname: Mapped[str]  = mapped_column(String(50), nullable=True)
    password: Mapped[str]  = mapped_column(String(50), nullable=False)

