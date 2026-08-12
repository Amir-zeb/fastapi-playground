# tests/test_auth.py
from uuid import uuid4
from fastapi.testclient import TestClient

def _register_payload() -> dict:
    return {
        "name": "Test User",
        "email": f"user-{uuid4().hex}@example.com",
        "password": "secret123",
        "age": 25,
        "gender": "male",
    }

def test_register_success(client: TestClient) -> None:
    response = client.post("/auth/register", json=_register_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == 201
    assert body["message"] == "user registered successfully"

def test_register_duplicate_email_returns_409(client: TestClient) -> None:
    payload = _register_payload()

    client.post("/auth/register", json=payload)               # first registration succeeds
    response = client.post("/auth/register", json=payload)    # second, same email

    assert response.status_code == 409
    body = response.json()
    assert body["status"] == 409
    assert body["message"] == "Email already registered"

def test_register_invalid_email_returns_422(client: TestClient) -> None:
    payload = _register_payload()
    payload["email"] = "not-an-email"

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422

def test_register_missing_field_returns_422(client: TestClient) -> None:
    payload = _register_payload()
    del payload["password"]

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422

def test_login_success(client: TestClient) -> None:
    payload = _register_payload()
    client.post("/auth/register", json=payload)   # create the user first

    response = client.post(
        "/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == 200
    assert body["message"] == "user logged in successfully"
    assert body["data"]["email"] == payload["email"]
    assert body["data"]["name"] == payload["name"]
    assert "password" not in body["data"]          # security check — password must never leak
    assert "access_token" in response.cookies 

def test_login_missing_field_return_422(client: TestClient) -> None:
    payload = _register_payload()
    client.post("/auth/register", json=payload)   # create the user first

    response = client.post(
        "/auth/login",
        json={"email": payload["email"]},
    )

    assert response.status_code == 422

def test_login_invalid_email_return_422(client: TestClient) -> None:
    payload = _register_payload()
    client.post("/auth/register", json=payload)   # create the user first

    response = client.post(
        "/auth/login",
        json={"email": "not-valid@email","password":payload["password"]},
    )

    assert response.status_code == 422

def test_login_invalid_credentials_return_401(client: TestClient) -> None:
    response = client.post(
        "/auth/login",
        json={"email": "example@email.com","password":"payload123456"},
    )

    assert response.status_code == 401

def test_me_success(client: TestClient) -> None:
    payload = _register_payload()
    client.post("/auth/register", json=payload)   # create the user first

    client.post(
        "/auth/login",
        json={"email": payload["email"],"password":payload["password"]},
    )
    
    response = client.get(
        "/auth/me",
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == 200
    assert body["message"] == "User details."
    assert body["data"]["email"] == payload["email"]
    assert body["data"]["name"] == payload["name"]
    assert "password" not in body["data"]          # security check — password must never leak

def test_me_without_login_returns_401(client: TestClient) -> None:
    response = client.get("/auth/me")

    assert response.status_code == 401