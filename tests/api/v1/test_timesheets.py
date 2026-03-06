import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash
from app.models.usuario import Usuario


async def create_user_and_login(client: AsyncClient, db: AsyncSession, email: str) -> str:
    user = Usuario(
        nombre="Fich",
        apellidos="Test",
        email=email,
        clave_hash=get_password_hash("pass1234"),
        rol="user",
        activo=True,
    )
    db.add(user)
    await db.flush()
    login = await client.post("/api/v1/auth/login", json={"email": email, "password": "pass1234"})
    return login.json()["access_token"]


@pytest.mark.asyncio
async def test_clock_in(client: AsyncClient, db_session: AsyncSession):
    token = await create_user_and_login(client, db_session, "user1@test.com")
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post("/api/v1/timesheets/clock-in", json={}, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "open"
    assert data["clock_out"] is None
    assert data["minutes_worked"] == 0


@pytest.mark.asyncio
async def test_clock_in_double_fails(client: AsyncClient, db_session: AsyncSession):
    token = await create_user_and_login(client, db_session, "user2@test.com")
    headers = {"Authorization": f"Bearer {token}"}

    await client.post("/api/v1/timesheets/clock-in", json={}, headers=headers)
    response = await client.post("/api/v1/timesheets/clock-in", json={}, headers=headers)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_clock_out(client: AsyncClient, db_session: AsyncSession):
    token = await create_user_and_login(client, db_session, "user3@test.com")
    headers = {"Authorization": f"Bearer {token}"}

    ci = await client.post("/api/v1/timesheets/clock-in", json={}, headers=headers)
    ts_id = ci.json()["timesheet_id"]

    co = await client.patch(f"/api/v1/timesheets/{ts_id}/clock-out", json={}, headers=headers)
    assert co.status_code == 200
    data = co.json()
    assert data["status"] == "closed"
    assert data["clock_out"] is not None
    assert data["minutes_worked"] >= 0


@pytest.mark.asyncio
async def test_logs_requires_admin(client: AsyncClient, db_session: AsyncSession):
    token = await create_user_and_login(client, db_session, "user4@test.com")
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/logs", headers=headers)
    assert response.status_code == 403
