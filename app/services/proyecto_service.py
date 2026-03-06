import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.proyecto_repository import proyecto_repository
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate
from app.models.proyecto import Proyecto
from app.services.log_service import write_log


async def create_proyecto(
    db: AsyncSession, data: ProyectoCreate, actor_id: Optional[uuid.UUID] = None
) -> Proyecto:
    proyecto = await proyecto_repository.create(db, data)
    await write_log(db, "proyectos", proyecto.proyecto_id, "create", actor_id,
                    new_data={"codigo": proyecto.codigo, "nombre": proyecto.nombre})
    return proyecto


async def update_proyecto(
    db: AsyncSession,
    proyecto_id: uuid.UUID,
    data: ProyectoUpdate,
    actor_id: Optional[uuid.UUID] = None,
) -> Optional[Proyecto]:
    proyecto = await proyecto_repository.get(db, proyecto_id)
    if not proyecto:
        return None
    old = {"nombre": proyecto.nombre}
    proyecto = await proyecto_repository.update(db, proyecto, data)
    await write_log(db, "proyectos", proyecto_id, "update", actor_id,
                    old_data=old, new_data={"nombre": proyecto.nombre})
    return proyecto


async def delete_proyecto(
    db: AsyncSession, proyecto_id: uuid.UUID, actor_id: Optional[uuid.UUID] = None
) -> bool:
    deleted = await proyecto_repository.delete(db, proyecto_id)
    if deleted:
        await write_log(db, "proyectos", proyecto_id, "delete", actor_id)
    return deleted
