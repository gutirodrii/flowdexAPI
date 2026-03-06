import uuid
from datetime import datetime
from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class Mercado(Base):
    __tablename__ = "mercado"

    mercado_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(server_default=text("now()"))
    updated_at: Mapped[datetime | None] = mapped_column(server_default=text("now()"))
