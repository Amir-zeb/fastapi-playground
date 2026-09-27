# tests/conftest.py
import asyncio
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from uuid import uuid4
from typing import AsyncGenerator, Generator, cast

from main import app
from app.dependencies import get_db
from app.models.user import Base
from app.models.user import UserModel

# In-memory SQLite — fast, fully isolated, gone the instant the process exits.
# StaticPool + check_same_thread=False: needed because SQLite's default behavior
# ties a connection to one thread, but TestClient can make requests across
# threads. StaticPool keeps a single shared connection alive for the whole
# test run instead of opening/closing per-request (which would lose the
# in-memory DB's contents between calls).
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
def create_test_db() -> Generator[None, None, None]:
    """Create all tables once before any test runs, drop them after the whole session."""

    async def _create() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def _drop() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(_create())
    yield
    asyncio.run(_drop())


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """A raw DB session against the same test engine the client fixture uses."""
    async with TestSessionLocal() as db:
        yield db


@pytest.fixture()
def regular_user(client: TestClient) -> dict:
    """Registers a plain user, returns their credentials."""
    payload = {
        "name": "Regular User",
        "email": f"user-{uuid4().hex}@example.com",
        "password": "secret123",
        "age": 25,
        "gender": "male",
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    return payload


@pytest.fixture()
async def admin_user(client: TestClient, db_session: AsyncSession) -> dict:
    """Registers a user, then promotes them to admin directly via DB."""
    payload = {
        "name": "Admin User",
        "email": f"admin-{uuid4().hex}@example.com",
        "password": "secret123",
        "age": 30,
        "gender": "female",
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201

    result = await db_session.execute(select(UserModel).filter(UserModel.email == payload["email"]))
    user = result.scalar_one()
    user.role = "admin"
    await db_session.commit()

    return payload


@pytest.fixture()
def logged_in_user(client: TestClient, regular_user: dict) -> TestClient:
    """A client already logged in as a regular user (cookie set)."""
    client.post("/auth/login", json={"email": regular_user["email"], "password": regular_user["password"]})
    return client


@pytest.fixture()
def logged_in_admin(client: TestClient, admin_user: dict) -> TestClient:
    """A client already logged in as an admin (cookie set)."""
    client.post("/auth/login", json={"email": admin_user["email"], "password": admin_user["password"]})
    return client


@pytest.fixture()
def seeded_users(client: TestClient) -> list[dict]:
    """Registers a fixed set of known users, returns their payloads."""
    users = [
        {"name": "Alice", "email": f"alice-{uuid4().hex}@example.com", "password": "secret123", "age": 28, "gender": "female"},
        {"name": "Bob", "email": f"bob-{uuid4().hex}@example.com", "password": "secret123", "age": 35, "gender": "male"},
        {"name": "Carol", "email": f"carol-{uuid4().hex}@example.com", "password": "secret123", "age": 42, "gender": "female"},
    ]

    for user in users:
        response = client.post("/auth/register", json=user)
        assert response.status_code == 201

    return users


@pytest.fixture()
def db_users(logged_in_admin: TestClient, seeded_users: list[dict]) -> list[dict]:
    response = logged_in_admin.get("/user/all")
    data = response.json()
    assert response.status_code == 200
    return cast(list[dict], data["data"])