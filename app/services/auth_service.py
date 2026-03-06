from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.usuario_repository import usuario_repository
from app.core.security import verify_password, create_access_token, get_password_hash
from app.models.usuario import Usuario


async def authenticate(db: AsyncSession, email: str, password: str) -> Optional[Usuario]:
    user = await usuario_repository.get_by_email(db, email)
    if not user or not user.activo:
        return None
    if not verify_password(password, user.clave_hash):
        return None
    user.last_login_at = datetime.now(timezone.utc)
    await db.flush()
    return user


def build_token(usuario: Usuario) -> str:
    return create_access_token({"sub": str(usuario.usuario_id), "rol": usuario.rol})
