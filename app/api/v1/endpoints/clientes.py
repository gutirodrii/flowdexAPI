import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.dependencies import get_current_user, require_admin
from app.models.usuario import Usuario
from app.repositories.cliente_repository import cliente_repository
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.services import cliente_service

router = APIRouter()


@router.get("", response_model=List[ClienteResponse])
async def list_clientes(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return await cliente_repository.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def create_cliente(
    data: ClienteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    try:
        return await cliente_service.create_cliente(db, data, actor_id=current_user.usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{cliente_id}", response_model=ClienteResponse)
async def read_cliente(
    cliente_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    cliente = await cliente_repository.get(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.patch("/{cliente_id}", response_model=ClienteResponse)
async def update_cliente(
    cliente_id: uuid.UUID,
    data: ClienteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    cliente = await cliente_service.update_cliente(db, cliente_id, data, actor_id=current_user.usuario_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente(
    cliente_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    deleted = await cliente_service.delete_cliente(db, cliente_id, actor_id=current_user.usuario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
