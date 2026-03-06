import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.dependencies import get_current_user, require_admin
from app.models.usuario import Usuario
from app.repositories.equipo_repository import equipo_repository
from app.schemas.equipo import EquipoCreate, EquipoUpdate, EquipoResponse, MiembroAdd, MiembroResponse
from app.services import equipo_service

router = APIRouter()


def _assert_owner_or_admin(equipo, current_user: Usuario):
    if current_user.rol != "admin" and equipo.created_by != current_user.usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este equipo")


@router.get("", response_model=List[EquipoResponse])
async def list_equipos(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return await equipo_repository.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=EquipoResponse, status_code=status.HTTP_201_CREATED)
async def create_equipo(
    data: EquipoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return await equipo_service.create_equipo(db, data, actor_id=current_user.usuario_id)


@router.get("/{equipo_id}", response_model=EquipoResponse)
async def read_equipo(
    equipo_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    equipo = await equipo_repository.get(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo


@router.patch("/{equipo_id}", response_model=EquipoResponse)
async def update_equipo(
    equipo_id: uuid.UUID,
    data: EquipoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    equipo = await equipo_repository.get(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    _assert_owner_or_admin(equipo, current_user)
    result = await equipo_service.update_equipo(db, equipo_id, data, actor_id=current_user.usuario_id)
    return result


@router.delete("/{equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipo(
    equipo_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    deleted = await equipo_service.delete_equipo(db, equipo_id, actor_id=current_user.usuario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")


@router.get("/{equipo_id}/miembros", response_model=List[MiembroResponse])
async def list_miembros(
    equipo_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    equipo = await equipo_repository.get(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return await equipo_repository.get_miembros(db, equipo_id)


@router.post("/{equipo_id}/miembros", response_model=MiembroResponse, status_code=status.HTTP_201_CREATED)
async def add_miembro(
    equipo_id: uuid.UUID,
    data: MiembroAdd,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    equipo = await equipo_repository.get(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    _assert_owner_or_admin(equipo, current_user)
    try:
        return await equipo_service.add_miembro(db, equipo_id, data, actor_id=current_user.usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{equipo_id}/miembros/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_miembro(
    equipo_id: uuid.UUID,
    usuario_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    equipo = await equipo_repository.get(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    _assert_owner_or_admin(equipo, current_user)
    removed = await equipo_service.remove_miembro(db, equipo_id, usuario_id, actor_id=current_user.usuario_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
