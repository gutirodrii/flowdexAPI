import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.timesheet_repository import timesheet_repository
from app.schemas.timesheet import ClockInRequest, ClockOutRequest
from app.models.timesheet import Timesheet
from app.services.log_service import write_log


async def clock_in(
    db: AsyncSession,
    usuario_id: uuid.UUID,
    data: ClockInRequest,
) -> Timesheet:
    open_ts = await timesheet_repository.get_open_for_user(db, usuario_id)
    if open_ts:
        raise ValueError("Ya tienes un fichaje abierto")

    ts = Timesheet(
        usuario_id=usuario_id,
        proyecto_id=data.proyecto_id,
        tarea_id=data.tarea_id,
        notas=data.notas,
        status="open",
        clock_in=datetime.now(timezone.utc),
        minutes_worked=0,
    )
    db.add(ts)
    await db.flush()
    await db.refresh(ts)
    await write_log(db, "timesheets", ts.timesheet_id, "create", usuario_id,
                    new_data={"status": "open"})
    return ts


async def clock_out(
    db: AsyncSession,
    timesheet_id: uuid.UUID,
    usuario_id: uuid.UUID,
    data: ClockOutRequest,
) -> Optional[Timesheet]:
    ts = await timesheet_repository.get(db, timesheet_id)
    if not ts or ts.usuario_id != usuario_id:
        return None
    if ts.status != "open":
        raise ValueError("El fichaje ya está cerrado")

    now = datetime.now(timezone.utc)
    clock_in_aware = ts.clock_in
    if clock_in_aware.tzinfo is None:
        clock_in_aware = clock_in_aware.replace(tzinfo=timezone.utc)

    ts.clock_out = now
    ts.minutes_worked = int((now - clock_in_aware).total_seconds() // 60)
    ts.status = "closed"
    if data.notas:
        ts.notas = data.notas

    await db.flush()
    await db.refresh(ts)
    await write_log(db, "timesheets", timesheet_id, "update", usuario_id,
                    new_data={"status": "closed", "minutes_worked": ts.minutes_worked})
    return ts
