import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.tarea_repository import tarea_repository
from app.schemas.tarea import TareaCreate, TareaUpdate
from app.models.tarea import Tarea
from app.services.log_service import write_log


async def create_tarea(
    db: AsyncSession,
    proyecto_id: uuid.UUID,
    data: TareaCreate,
    actor_id: Optional[uuid.UUID] = None,
) -> Tarea:
    tarea = Tarea(
        proyecto_id=proyecto_id,
        titulo=data.titulo,
        descripcion=data.descripcion,
        estado=data.estado,
        prioridad=data.prioridad,
        asignado_a=data.asignado_a,
        fecha_vencimiento=data.fecha_vencimiento,
        creada_por=actor_id,
    )
    db.add(tarea)
    await db.flush()
    await db.refresh(tarea)
    await write_log(db, "tareas", tarea.tarea_id, "create", actor_id,
                    new_data={"titulo": tarea.titulo, "proyecto_id": str(proyecto_id)})
    return tarea


async def update_tarea(
    db: AsyncSession,
    tarea_id: uuid.UUID,
    data: TareaUpdate,
    actor_id: Optional[uuid.UUID] = None,
) -> Optional[Tarea]:
    tarea = await tarea_repository.get(db, tarea_id)
    if not tarea:
        return None
    old = {"estado": tarea.estado, "prioridad": tarea.prioridad}
    tarea = await tarea_repository.update(db, tarea, data)
    await write_log(db, "tareas", tarea_id, "update", actor_id,
                    old_data=old, new_data={"estado": tarea.estado})
    return tarea


async def delete_tarea(
    db: AsyncSession, tarea_id: uuid.UUID, actor_id: Optional[uuid.UUID] = None
) -> bool:
    deleted = await tarea_repository.delete(db, tarea_id)
    if deleted:
        await write_log(db, "tareas", tarea_id, "delete", actor_id)
    return deleted
