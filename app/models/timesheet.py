import uuid
from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, text, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class Timesheet(Base):
    __tablename__ = "timesheets"
    __table_args__ = (
        CheckConstraint("clock_out IS NULL OR clock_out >= clock_in", name="ck_clock_order"),
    )

    timesheet_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.usuario_id", ondelete="CASCADE"),
        nullable=False,
    )
    proyecto_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("proyectos.proyecto_id", ondelete="SET NULL"),
        nullable=True,
    )
    tarea_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tareas.tarea_id", ondelete="SET NULL"),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(String, nullable=False, server_default="open")
    clock_in: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    clock_out: Mapped[datetime | None] = mapped_column(nullable=True)
    minutes_worked: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    notas: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(server_default=func.now())
