from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from app.repositories.base import BaseRepository


class ClienteRepository(BaseRepository[Cliente, ClienteCreate, ClienteUpdate]):
    def __init__(self):
        super().__init__(Cliente, "cliente_id")

    async def get_by_nif(self, db: AsyncSession, nif: str) -> Optional[Cliente]:
        result = await db.execute(select(Cliente).where(Cliente.nif == nif))
        return result.scalars().first()


cliente_repository = ClienteRepository()
