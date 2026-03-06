import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.equipo_repository import equipo_repository
from app.schemas.equipo import EquipoCreate, EquipoUpdate, MiembroAdd
from app.models.equipo import Equipo, EquipoUsuario
from app.services.log_service import write_log


async def create_equipo(
    db: AsyncSession, data: EquipoCreate, actor_id: Optional[uuid.UUID] = None
) -> Equipo:
    equipo = Equipo(
        nombre=data.nombre,
        descripcion=data.descripcion,
        created_by=actor_id,
    )
    db.add(equipo)
    await db.flush()
    await db.refresh(equipo)
    await write_log(db, "equipos", equipo.equipo_id, "create", actor_id,
                    new_data={"nombre": equipo.nombre})
    return equipo


async def update_equipo(
    db: AsyncSession,
    equipo_id: uuid.UUID,
    data: EquipoUpdate,
    actor_id: Optional[uuid.UUID] = None,
) -> Optional[Equipo]:
    equipo = await equipo_repository.get(db, equipo_id)
    if not equipo:
        return None
    old = {"nombre": equipo.nombre}
    equipo = await equipo_repository.update(db, equipo, data)
    await write_log(db, "equipos", equipo_id, "update", actor_id,
                    old_data=old, new_data={"nombre": equipo.nombre})
    return equipo


async def delete_equipo(
    db: AsyncSession, equipo_id: uuid.UUID, actor_id: Optional[uuid.UUID] = None
) -> bool:
    deleted = await equipo_repository.delete(db, equipo_id)
    if deleted:
        await write_log(db, "equipos", equipo_id, "delete", actor_id)
    return deleted


async def add_miembro(
    db: AsyncSession,
    equipo_id: uuid.UUID,
    data: MiembroAdd,
    actor_id: Optional[uuid.UUID] = None,
) -> EquipoUsuario:
    existing = await equipo_repository.get_miembro(db, equipo_id, data.usuario_id)
    if existing:
        raise ValueError("Usuario ya es miembro del equipo")
    miembro = await equipo_repository.add_miembro(
        db, equipo_id, data.usuario_id, data.rol_equipo
    )
    await write_log(db, "equipo_usuarios", equipo_id, "create", actor_id,
                    new_data={"usuario_id": str(data.usuario_id), "rol": data.rol_equipo})
    return miembro


async def remove_miembro(
    db: AsyncSession,
    equipo_id: uuid.UUID,
    usuario_id: uuid.UUID,
    actor_id: Optional[uuid.UUID] = None,
) -> bool:
    removed = await equipo_repository.remove_miembro(db, equipo_id, usuario_id)
    if removed:
        await write_log(db, "equipo_usuarios", equipo_id, "delete", actor_id,
                        old_data={"usuario_id": str(usuario_id)})
    return removed
