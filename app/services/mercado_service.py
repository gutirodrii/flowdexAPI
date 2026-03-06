import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.mercado_repository import mercado_repository
from app.schemas.mercado import MercadoCreate, MercadoUpdate
from app.models.mercado import Mercado
from app.services.log_service import write_log


async def create_mercado(
    db: AsyncSession, data: MercadoCreate, actor_id: Optional[uuid.UUID] = None
) -> Mercado:
    mercado = await mercado_repository.create(db, data)
    await write_log(db, "mercado", mercado.mercado_id, "create", actor_id,
                    new_data={"nombre": mercado.nombre})
    return mercado


async def update_mercado(
    db: AsyncSession,
    mercado_id: uuid.UUID,
    data: MercadoUpdate,
    actor_id: Optional[uuid.UUID] = None,
) -> Optional[Mercado]:
    mercado = await mercado_repository.get(db, mercado_id)
    if not mercado:
        return None
    old = {"nombre": mercado.nombre}
    mercado = await mercado_repository.update(db, mercado, data)
    await write_log(db, "mercado", mercado_id, "update", actor_id,
                    old_data=old, new_data={"nombre": mercado.nombre})
    return mercado


async def delete_mercado(
    db: AsyncSession, mercado_id: uuid.UUID, actor_id: Optional[uuid.UUID] = None
) -> bool:
    deleted = await mercado_repository.delete(db, mercado_id)
    if deleted:
        await write_log(db, "mercado", mercado_id, "delete", actor_id)
    return deleted
