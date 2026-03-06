import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.dependencies import get_current_user, require_admin
from app.models.usuario import Usuario
from app.repositories.mercado_repository import mercado_repository
from app.schemas.mercado import MercadoCreate, MercadoUpdate, MercadoResponse
from app.services import mercado_service

router = APIRouter()


@router.get("", response_model=List[MercadoResponse])
async def list_mercados(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return await mercado_repository.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=MercadoResponse, status_code=status.HTTP_201_CREATED)
async def create_mercado(
    data: MercadoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    return await mercado_service.create_mercado(db, data, actor_id=current_user.usuario_id)


@router.get("/{mercado_id}", response_model=MercadoResponse)
async def read_mercado(
    mercado_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    mercado = await mercado_repository.get(db, mercado_id)
    if not mercado:
        raise HTTPException(status_code=404, detail="Mercado no encontrado")
    return mercado


@router.patch("/{mercado_id}", response_model=MercadoResponse)
async def update_mercado(
    mercado_id: uuid.UUID,
    data: MercadoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    mercado = await mercado_service.update_mercado(db, mercado_id, data, actor_id=current_user.usuario_id)
    if not mercado:
        raise HTTPException(status_code=404, detail="Mercado no encontrado")
    return mercado


@router.delete("/{mercado_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mercado(
    mercado_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    deleted = await mercado_service.delete_mercado(db, mercado_id, actor_id=current_user.usuario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Mercado no encontrado")
