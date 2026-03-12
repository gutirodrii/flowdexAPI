import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class Equipo(Base):
    __tablename__ = "equipos"

    equipo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String, nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.usuario_id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime | None] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(server_default=func.now())


class EquipoUsuario(Base):
    __tablename__ = "equipo_usuarios"

    equipo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("equipos.equipo_id", ondelete="CASCADE"),
        primary_key=True,
    )
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.usuario_id", ondelete="CASCADE"),
        primary_key=True,
    )
    rol_equipo: Mapped[str] = mapped_column(String, server_default="member")
    joined_at: Mapped[datetime | None] = mapped_column(server_default=func.now())
