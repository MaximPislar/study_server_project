import uuid
import datetime

from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from fastapi_app.database.models import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    # id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jti: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4
    )
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)

    issued_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    device_info: Mapped[str] = mapped_column(String, nullable=True)  # optional

    @property
    def user_id_str(self):
        """Возвращает ID юзера как строку"""
        return str(self.user_id) if self.user_id else None

    @property
    def jti_str(self):
        """Возвращает JTI как строку"""
        return str(self.jti) if self.jti else None
