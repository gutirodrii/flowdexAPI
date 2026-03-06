import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.cliente_repository import cliente_repository
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from app.models.cliente import Cliente
from app.services.log_service import write_log


async def create_cliente(
    db: AsyncSession, data: ClienteCreate, actor_id: Optional[uuid.UUID] = None
) -> Cliente:
    existing = await cliente_repository.get_by_nif(db, data.nif)
    if existing:
        raise ValueError("NIF ya registrado")
    cliente = await cliente_repository.create(db, data)
    await write_log(db, "clientes", cliente.cliente_id, "create", actor_id,
                    new_data={"nif": cliente.nif})
    return cliente


async def update_cliente(
    db: AsyncSession,
    cliente_id: uuid.UUID,
    data: ClienteUpdate,
    actor_id: Optional[uuid.UUID] = None,
) -> Optional[Cliente]:
    cliente = await cliente_repository.get(db, cliente_id)
    if not cliente:
        return None
    old = {"nif": cliente.nif, "activo": cliente.activo}
    cliente = await cliente_repository.update(db, cliente, data)
    await write_log(db, "clientes", cliente_id, "update", actor_id,
                    old_data=old, new_data={"activo": cliente.activo})
    return cliente


async def delete_cliente(
    db: AsyncSession, cliente_id: uuid.UUID, actor_id: Optional[uuid.UUID] = None
) -> bool:
    deleted = await cliente_repository.delete(db, cliente_id)
    if deleted:
        await write_log(db, "clientes", cliente_id, "delete", actor_id)
    return deleted
