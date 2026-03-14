import pytest
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models.usuario import Usuario
from scripts import create_admin as create_admin_module


@pytest.mark.asyncio
async def test_ensure_admin_creates_admin(engine):
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        await session.execute(delete(Usuario))
        await session.commit()

    create_admin_module.AsyncSessionLocal = session_factory
    create_admin_module.settings.ADMIN_SEED_NOMBRE = "Admin"
    create_admin_module.settings.ADMIN_SEED_APELLIDOS = "Flowdex"
    create_admin_module.settings.ADMIN_SEED_EMAIL = "admin@flowdex.es"
    create_admin_module.settings.ADMIN_SEED_PASSWORD = "Admin1234!"

    created = await create_admin_module.ensure_admin()
    assert created is True

    async with session_factory() as session:
        result = await session.execute(select(Usuario).where(Usuario.email == "admin@flowdex.es"))
        admin = result.scalar_one()

    assert admin.nombre == "Admin"
    assert admin.apellidos == "Flowdex"
    assert admin.rol == "admin"
    assert admin.activo is True
    assert admin.clave_hash != "Admin1234!"


@pytest.mark.asyncio
async def test_ensure_admin_is_idempotent(engine):
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        await session.execute(delete(Usuario))
        await session.commit()

    create_admin_module.AsyncSessionLocal = session_factory
    create_admin_module.settings.ADMIN_SEED_NOMBRE = "Admin"
    create_admin_module.settings.ADMIN_SEED_APELLIDOS = "Flowdex"
    create_admin_module.settings.ADMIN_SEED_EMAIL = "admin@flowdex.es"
    create_admin_module.settings.ADMIN_SEED_PASSWORD = "Admin1234!"

    await create_admin_module.ensure_admin()
    created = await create_admin_module.ensure_admin()

    assert created is False

    async with session_factory() as session:
        result = await session.execute(
            select(func.count()).select_from(Usuario).where(Usuario.email == "admin@flowdex.es")
        )
        count = result.scalar_one()

    assert count == 1
