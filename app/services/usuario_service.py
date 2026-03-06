import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.usuario_repository import usuario_repository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.models.usuario import Usuario
from app.core.security import get_password_hash
from app.services.log_service import write_log


async def create_usuario(
    db: AsyncSession, data: UsuarioCreate, actor_id: Optional[uuid.UUID] = None
) -> Usuario:
    if data.email:
        existing_email = await usuario_repository.get_by_email(db, data.email)
        if existing_email:
            raise ValueError("Email ya registrado")

    create_data = data.model_dump(exclude={"password"})
    create_data["clave_hash"] = get_password_hash(data.password)

    from app.schemas.usuario import UsuarioBase
    from pydantic import BaseModel

    class _InternalCreate(BaseModel):
        model_config = {"arbitrary_types_allowed": True}

    usuario = Usuario(**create_data)
    db.add(usuario)
    await db.flush()
    await db.refresh(usuario)

    await write_log(
        db, "usuarios", usuario.usuario_id, "create", actor_id,
        new_data={"email": usuario.email, "rol": usuario.rol}
    )
    return usuario


async def update_usuario(
    db: AsyncSession,
    usuario_id: uuid.UUID,
    data: UsuarioUpdate,
    actor_id: Optional[uuid.UUID] = None,
) -> Optional[Usuario]:
    usuario = await usuario_repository.get(db, usuario_id)
    if not usuario:
        return None

    old_data = {"email": usuario.email, "rol": usuario.rol, "activo": usuario.activo}
    update_fields = data.model_dump(exclude_unset=True, exclude={"password"})

    if data.password:
        update_fields["clave_hash"] = get_password_hash(data.password)

    for field, value in update_fields.items():
        setattr(usuario, field, value)

    await db.flush()
    await db.refresh(usuario)

    await write_log(
        db, "usuarios", usuario.usuario_id, "update", actor_id,
        old_data=old_data,
        new_data={"email": usuario.email, "rol": usuario.rol, "activo": usuario.activo}
    )
    return usuario


async def soft_delete_usuario(
    db: AsyncSession, usuario_id: uuid.UUID, actor_id: Optional[uuid.UUID] = None
) -> bool:
    usuario = await usuario_repository.get(db, usuario_id)
    if not usuario:
        return False
    usuario.activo = False
    await db.flush()
    await write_log(db, "usuarios", usuario_id, "delete", actor_id)
    return True
