import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.usuario import Usuario
from app.repositories.timesheet_repository import timesheet_repository
from app.schemas.timesheet import ClockInRequest, ClockOutRequest, TimesheetResponse
from app.services import timesheet_service

router = APIRouter()


@router.post("/clock-in", response_model=TimesheetResponse, status_code=status.HTTP_201_CREATED)
async def clock_in(
    data: ClockInRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        return await timesheet_service.clock_in(db, current_user.usuario_id, data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.patch("/{timesheet_id}/clock-out", response_model=TimesheetResponse)
async def clock_out(
    timesheet_id: uuid.UUID,
    data: ClockOutRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        ts = await timesheet_service.clock_out(db, timesheet_id, current_user.usuario_id, data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    if ts is None:
        raise HTTPException(status_code=404, detail="Fichaje no encontrado")
    return ts


@router.get("", response_model=List[TimesheetResponse])
async def list_timesheets(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    if current_user.rol == "admin":
        return await timesheet_repository.get_multi(db, skip=skip, limit=limit)
    return await timesheet_repository.get_by_usuario(db, current_user.usuario_id, skip=skip, limit=limit)


@router.get("/{timesheet_id}", response_model=TimesheetResponse)
async def read_timesheet(
    timesheet_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    ts = await timesheet_repository.get(db, timesheet_id)
    if not ts:
        raise HTTPException(status_code=404, detail="Fichaje no encontrado")
    if current_user.rol != "admin" and ts.usuario_id != current_user.usuario_id:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return ts
