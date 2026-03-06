import uuid
from datetime import date, datetime
from sqlalchemy import Date, String, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class Proyecto(Base):
    __tablename__ = "proyectos"

    proyecto_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    codigo: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String, nullable=True)
    mercado_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("mercado.mercado_id", ondelete="SET NULL"),
        nullable=True,
    )
    cliente_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("clientes.cliente_id", ondelete="SET NULL"),
        nullable=True,
    )
    equipo_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("equipos.equipo_id", ondelete="SET NULL"),
        nullable=True,
    )
    owner_usuario_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.usuario_id", ondelete="SET NULL"),
        nullable=True,
    )
    fecha_inicio: Mapped[date | None] = mapped_column(Date, nullable=True)
    fecha_fin: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(server_default=text("now()"))
    updated_at: Mapped[datetime | None] = mapped_column(server_default=text("now()"))
