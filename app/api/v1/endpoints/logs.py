from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.dependencies import require_admin
from app.models.usuario import Usuario
from app.repositories.log_repository import log_repository
from app.schemas.log import LogResponse

router = APIRouter()


@router.get("", response_model=List[LogResponse])
async def list_logs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    return await log_repository.get_multi_ordered(db, skip=skip, limit=limit)
