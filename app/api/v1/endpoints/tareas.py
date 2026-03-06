import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.dependencies import get_current_user, require_admin
from app.models.usuario import Usuario
from app.repositories.proyecto_repository import proyecto_repository
from app.repositories.tarea_repository import tarea_repository
from app.schemas.tarea import TareaCreate, TareaUpdate, TareaResponse
from app.services import tarea_service

router = APIRouter()


@router.get("/proyectos/{proyecto_id}/tareas", response_model=List[TareaResponse])
async def list_tareas(
    proyecto_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    proyecto = await proyecto_repository.get(db, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return await tarea_repository.get_by_proyecto(db, proyecto_id, skip=skip, limit=limit)


@router.post("/proyectos/{proyecto_id}/tareas", response_model=TareaResponse, status_code=status.HTTP_201_CREATED)
async def create_tarea(
    proyecto_id: uuid.UUID,
    data: TareaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    proyecto = await proyecto_repository.get(db, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return await tarea_service.create_tarea(db, proyecto_id, data, actor_id=current_user.usuario_id)


@router.get("/tareas/{tarea_id}", response_model=TareaResponse)
async def read_tarea(
    tarea_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    tarea = await tarea_repository.get(db, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea


@router.patch("/tareas/{tarea_id}", response_model=TareaResponse)
async def update_tarea(
    tarea_id: uuid.UUID,
    data: TareaUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    tarea = await tarea_repository.get(db, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    if current_user.rol != "admin" and tarea.asignado_a != current_user.usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta tarea")
    result = await tarea_service.update_tarea(db, tarea_id, data, actor_id=current_user.usuario_id)
    return result


@router.delete("/tareas/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tarea(
    tarea_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    deleted = await tarea_service.delete_tarea(db, tarea_id, actor_id=current_user.usuario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
