"""Seed idempotente para asegurar un usuario admin en la base de datos."""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.core.config import get_settings
from app.core.security import get_password_hash
from app.models.usuario import Usuario

settings = get_settings()


async def ensure_admin() -> bool:
    if not settings.ADMIN_SEED_PASSWORD:
        raise ValueError("ADMIN_SEED_PASSWORD es obligatorio para crear el admin")

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Usuario).where(Usuario.email == settings.ADMIN_SEED_EMAIL)
        )
        existing = result.scalar_one_or_none()

        if existing:
            print(f"Ya existe un usuario admin con email '{settings.ADMIN_SEED_EMAIL}'.")
            return False

        admin = Usuario(
            nombre=settings.ADMIN_SEED_NOMBRE,
            apellidos=settings.ADMIN_SEED_APELLIDOS,
            email=settings.ADMIN_SEED_EMAIL,
            clave_hash=get_password_hash(settings.ADMIN_SEED_PASSWORD),
            rol="admin",
            activo=True,
        )
        session.add(admin)
        await session.commit()
        await session.refresh(admin)

        print(f"Usuario admin creado exitosamente.")
        print(f"  ID:    {admin.usuario_id}")
        print(f"  Email: {admin.email}")
        print(f"  Rol:   {admin.rol}")
        return True


if __name__ == "__main__":
    asyncio.run(ensure_admin())
