# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from uuid import uuid4

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
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    """Create all tables once before any test runs, drop them after the whole session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture()
def db_session():
    """A raw DB session against the same test engine the client fixture uses."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


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
def admin_user(client: TestClient, db_session: Session) -> dict:
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

    user = db_session.query(UserModel).filter(UserModel.email == payload["email"]).first()
    user.role = "admin"
    db_session.commit()

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
        {
            "name": "Alice",
            "email": f"alice-{uuid4().hex}@example.com",
            "password": "secret123",
            "age": 28,
            "gender": "female",
        },
        {
            "name": "Bob",
            "email": f"bob-{uuid4().hex}@example.com",
            "password": "secret123",
            "age": 35,
            "gender": "male",
        },
        {
            "name": "Carol",
            "email": f"carol-{uuid4().hex}@example.com",
            "password": "secret123",
            "age": 42,
            "gender": "female",
        },
    ]

    for user in users:
        response = client.post("/auth/register", json=user)
        assert response.status_code == 201

    return users

# Adding seeded_users as a parameter 
# (even though you don't directly use the variable inside the function body) 
# forces pytest to resolve and run it first, guaranteeing Alice/Bob/Carol 
# actually exist before /user/all is called.
@pytest.fixture()
def db_users(logged_in_admin:TestClient,seeded_users: list[dict]) -> list[dict]:
    response = logged_in_admin.get("/user/all")
    data=response.json()
    assert response.status_code == 200
    return data["data"]