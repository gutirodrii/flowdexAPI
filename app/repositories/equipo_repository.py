import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.equipo import Equipo, EquipoUsuario
from app.schemas.equipo import EquipoCreate, EquipoUpdate
from app.repositories.base import BaseRepository


class EquipoRepository(BaseRepository[Equipo, EquipoCreate, EquipoUpdate]):
    def __init__(self):
        super().__init__(Equipo, "equipo_id")

    async def add_miembro(
        self,
        db: AsyncSession,
        equipo_id: uuid.UUID,
        usuario_id: uuid.UUID,
        rol_equipo: str = "member",
    ) -> EquipoUsuario:
        miembro = EquipoUsuario(
            equipo_id=equipo_id, usuario_id=usuario_id, rol_equipo=rol_equipo
        )
        db.add(miembro)
        await db.flush()
        await db.refresh(miembro)
        return miembro

    async def remove_miembro(
        self, db: AsyncSession, equipo_id: uuid.UUID, usuario_id: uuid.UUID
    ) -> bool:
        result = await db.execute(
            select(EquipoUsuario).where(
                EquipoUsuario.equipo_id == equipo_id,
                EquipoUsuario.usuario_id == usuario_id,
            )
        )
        miembro = result.scalars().first()
        if miembro is None:
            return False
        await db.delete(miembro)
        return True

    async def get_miembros(
        self, db: AsyncSession, equipo_id: uuid.UUID
    ) -> List[EquipoUsuario]:
        result = await db.execute(
            select(EquipoUsuario).where(EquipoUsuario.equipo_id == equipo_id)
        )
        return list(result.scalars().all())

    async def get_miembro(
        self, db: AsyncSession, equipo_id: uuid.UUID, usuario_id: uuid.UUID
    ) -> Optional[EquipoUsuario]:
        result = await db.execute(
            select(EquipoUsuario).where(
                EquipoUsuario.equipo_id == equipo_id,
                EquipoUsuario.usuario_id == usuario_id,
            )
        )
        return result.scalars().first()


equipo_repository = EquipoRepository()
