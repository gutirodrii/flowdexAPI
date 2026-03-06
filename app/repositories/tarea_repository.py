import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tarea import Tarea
from app.schemas.tarea import TareaCreate, TareaUpdate
from app.repositories.base import BaseRepository


class TareaRepository(BaseRepository[Tarea, TareaCreate, TareaUpdate]):
    def __init__(self):
        super().__init__(Tarea, "tarea_id")

    async def get_by_proyecto(
        self, db: AsyncSession, proyecto_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Tarea]:
        result = await db.execute(
            select(Tarea)
            .where(Tarea.proyecto_id == proyecto_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())


tarea_repository = TareaRepository()
