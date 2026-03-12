import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.dependencies import get_current_user, require_admin
from app.models.usuario import Usuario
from app.repositories.usuario_repository import usuario_repository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services import usuario_service

router = APIRouter()


@router.get("/me", response_model=UsuarioResponse)
async def read_me(current_user: Usuario = Depends(get_current_user)):
    return current_user


@router.get("", response_model=List[UsuarioResponse])
async def list_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    return await usuario_repository.get_multi(db, skip=skip, limit=limit)


@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def create_usuario(
    data: UsuarioCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    try:
        return await usuario_service.create_usuario(db, data, actor_id=current_user.usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def read_usuario(
    usuario_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    usuario = await usuario_repository.get(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.patch("/{usuario_id}", response_model=UsuarioResponse)
async def update_usuario(
    usuario_id: uuid.UUID,
    data: UsuarioUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    try:
        usuario = await usuario_service.update_usuario(
            db, usuario_id, data, actor_id=current_user.usuario_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(
    usuario_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(require_admin),
):
    deleted = await usuario_service.soft_delete_usuario(db, usuario_id, actor_id=current_user.usuario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
