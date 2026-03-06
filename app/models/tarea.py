import uuid
from datetime import date, datetime
from sqlalchemy import Date, String, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class Tarea(Base):
    __tablename__ = "tareas"

    tarea_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    proyecto_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("proyectos.proyecto_id", ondelete="CASCADE"),
        nullable=False,
    )
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String, nullable=True)
    estado: Mapped[str] = mapped_column(String, nullable=False, server_default="todo")
    prioridad: Mapped[str] = mapped_column(String, nullable=False, server_default="medium")
    asignado_a: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.usuario_id", ondelete="SET NULL"),
        nullable=True,
    )
    creada_por: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.usuario_id", ondelete="SET NULL"),
        nullable=True,
    )
    fecha_vencimiento: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(server_default=text("now()"))
    updated_at: Mapped[datetime | None] = mapped_column(server_default=text("now()"))
