import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash
from app.models.usuario import Usuario


async def create_test_user(db: AsyncSession, email: str = "test@example.com", rol: str = "user") -> Usuario:
    user = Usuario(
        nombre="Test",
        apellidos="User",
        email=email,
        clave_hash=get_password_hash("password123"),
        rol=rol,
        activo=True,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, db_session: AsyncSession):
    await create_test_user(db_session)
    response = await client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, db_session: AsyncSession):
    response = await client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "wrong"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_requires_auth(client: AsyncClient):
    response = await client.get("/api/v1/usuarios/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_returns_user(client: AsyncClient, db_session: AsyncSession):
    await create_test_user(db_session, email="otro@example.com")
    login = await client.post("/api/v1/auth/login", json={"email": "otro@example.com", "password": "password123"})
    token = login.json()["access_token"]

    response = await client.get(
        "/api/v1/usuarios/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "otro@example.com"
