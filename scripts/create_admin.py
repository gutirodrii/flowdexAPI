"""Script para crear un usuario admin en la base de datos."""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.usuario import Usuario


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


ADMIN_NOMBRE = "Admin"
ADMIN_APELLIDOS = "Flowdex"
ADMIN_EMAIL = "admin@flowdex.com"
ADMIN_PASSWORD = "Admin1234!"


async def create_admin():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Usuario).where(Usuario.email == ADMIN_EMAIL)
        )
        existing = result.scalar_one_or_none()

        if existing:
            print(f"Ya existe un usuario con email '{ADMIN_EMAIL}'.")
            return

        admin = Usuario(
            nombre=ADMIN_NOMBRE,
            apellidos=ADMIN_APELLIDOS,
            email=ADMIN_EMAIL,
            clave_hash=hash_password(ADMIN_PASSWORD),
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


if __name__ == "__main__":
    asyncio.run(create_admin())
