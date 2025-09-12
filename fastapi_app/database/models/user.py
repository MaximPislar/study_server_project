import uuid

from sqlalchemy import String, true
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from fastapi_app.database.models import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(server_default=true(), nullable=False)
