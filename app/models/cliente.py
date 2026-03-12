import uuid
from datetime import datetime
from sqlalchemy import Boolean, String, text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class Cliente(Base):
    __tablename__ = "clientes"

    cliente_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    nif: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    nombre_comercial: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    telefono: Mapped[str | None] = mapped_column(String, nullable=True)
    direccion: Mapped[str | None] = mapped_column(String, nullable=True)
    ciudad: Mapped[str | None] = mapped_column(String, nullable=True)
    provincia: Mapped[str | None] = mapped_column(String, nullable=True)
    cp: Mapped[str | None] = mapped_column(String, nullable=True)
    pais: Mapped[str] = mapped_column(String, nullable=False, server_default="ES")
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    created_at: Mapped[datetime | None] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(server_default=func.now())
