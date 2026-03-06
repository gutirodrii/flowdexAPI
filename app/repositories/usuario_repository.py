from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.repositories.base import BaseRepository


class UsuarioRepository(BaseRepository[Usuario, UsuarioCreate, UsuarioUpdate]):
    def __init__(self):
        super().__init__(Usuario, "usuario_id")

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[Usuario]:
        result = await db.execute(select(Usuario).where(Usuario.email == email))
        return result.scalars().first()


usuario_repository = UsuarioRepository()
