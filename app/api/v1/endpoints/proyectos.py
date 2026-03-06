import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.dependencies import get_current_user, require_admin
from app.models.usuario import Usuario
from app.repositories.proyecto_repository import proyecto_repository
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate, ProyectoResponse
from app.services import proyecto_service

router = APIRouter()


def _assert_owner_or_admin(proyecto, current_user: Usuario):
    if current_user.rol != "admin" and proyecto.owner_usuario_id != current_user.usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este proyecto")


@router.get("", response_model=List[ProyectoResponse])
async def list_proyectos(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return await proyecto_repository.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=ProyectoResponse, status_code=status.HTTP_201_CREATED)
async def create_proyecto(
    data: ProyectoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return await proyecto_service.create_proyecto(db, data, actor_id=current_user.usuario_id)


@router.get("/{proyecto_id}", response_model=ProyectoResponse)
async def read_proyecto(
    proyecto_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    proyecto = await proyecto_repository.get(db, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto


@router.patch("/{proyecto_id}", response_model=ProyectoResponse)
async def update_proyecto(
    proyecto_id: uuid.UUID,
    data: ProyectoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    proyecto = await proyecto_repository.get(db, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    _assert_owner_or_admin(proyecto, current_user)
    result = await proyecto_service.update_proyecto(db, proyecto_id, data, actor_id=current_user.usuario_id)
    return result


@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_proyecto(
    proyecto_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    deleted = await proyecto_service.delete_proyecto(db, proyecto_id, actor_id=current_user.usuario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
