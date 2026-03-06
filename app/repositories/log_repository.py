from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.log import Log
from app.repositories.base import BaseRepository
from pydantic import BaseModel


class LogRepository(BaseRepository[Log, BaseModel, BaseModel]):
    def __init__(self):
        super().__init__(Log, "log_id")

    async def get_multi_ordered(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Log]:
        result = await db.execute(
            select(Log).order_by(Log.created_at.desc()).offset(skip).limit(limit)
        )
        return list(result.scalars().all())


log_repository = LogRepository()
