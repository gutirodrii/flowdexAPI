import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.timesheet import Timesheet
from app.schemas.timesheet import ClockInRequest, ClockOutRequest
from app.repositories.base import BaseRepository


class TimesheetRepository(BaseRepository[Timesheet, ClockInRequest, ClockOutRequest]):
    def __init__(self):
        super().__init__(Timesheet, "timesheet_id")

    async def get_open_for_user(
        self, db: AsyncSession, usuario_id: uuid.UUID
    ) -> Optional[Timesheet]:
        result = await db.execute(
            select(Timesheet).where(
                Timesheet.usuario_id == usuario_id,
                Timesheet.status == "open",
                Timesheet.clock_out.is_(None),
            )
        )
        return result.scalars().first()

    async def get_by_usuario(
        self,
        db: AsyncSession,
        usuario_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Timesheet]:
        result = await db.execute(
            select(Timesheet)
            .where(Timesheet.usuario_id == usuario_id)
            .order_by(Timesheet.clock_in.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())


timesheet_repository = TimesheetRepository()
