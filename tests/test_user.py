# tests/test_user.py
from fastapi.testclient import TestClient
from uuid import uuid4

def _register_payload() -> dict:
    return {
        "name": "Test User",
        "email": f"user-{uuid4().hex}@example.com",
        "password": "secret123",
        "age": 25,
        "gender": "male",
    }

def test_admin_can_list_users(logged_in_admin: TestClient) -> None:
    response = logged_in_admin.get("/user/all")
    assert response.status_code == 200

def test_regular_user_cannot_list_users(logged_in_user: TestClient) -> None:
    response = logged_in_user.get("/user/all")
    assert response.status_code == 403

def test_admin_can_list_all_users(logged_in_admin: TestClient, admin_user: dict, seeded_users: list[dict]) -> None:
    response = logged_in_admin.get("/user/all")

    assert response.status_code == 200
    body = response.json()

    returned_emails = {user["email"] for user in body["data"]}
    expected_emails = {user["email"] for user in seeded_users} | {admin_user["email"]}

    assert expected_emails.issubset(returned_emails)

def test_admin_can_find_specific_user_by_id(logged_in_admin: TestClient, db_users: list[dict]) -> None:
    # short way of writing a for loop that stops when it finds the first match.
    bob = next(u for u in db_users if u["name"] == "Bob")

    id= bob["id"]
    response = logged_in_admin.get(f"/user/{id}")
    body = response.json()
    
    assert response.status_code == 200
    assert body["data"]["name"] == "Bob"
    assert body["data"]["age"] == 35
    assert body["data"]["gender"] == "male"

def test_admin_get_user_by_invalid_id(logged_in_admin: TestClient) -> None:
    response = logged_in_admin.get("/user/1000")
    assert response.status_code == 404

def test_admin_delete_user_by_id(logged_in_admin: TestClient, db_users: list[dict]) -> None:
    # short way of writing a for loop that stops when it finds the first match.
    bob = next(u for u in db_users if u["name"] == "Bob")

    id= bob["id"]
    response = logged_in_admin.delete(f"/user/{id}")
    body = response.json()
    assert response.status_code == 200
    assert body["data"]["user_id"]==id
    assert body["message"]=="User deleted successfully"
    
def test_admin_delete_user_by_invalid_id(logged_in_admin: TestClient) -> None:
    response = logged_in_admin.delete("/user/1000")
    assert response.status_code == 404
    
def test_admin_create_new_user_success(logged_in_admin: TestClient) -> None:
    d =_register_payload()
    response = logged_in_admin.post("/user/create", json=d)

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == 201
    assert body["message"] == "User created successfully"
    assert body["data"]["name"] == d["name"]
    assert body["data"]["email"] == d["email"]
    assert "password" not in body["data"]          # security check — password must never leak

def test_admin_create_new_user_with_existing_email(logged_in_admin: TestClient, seeded_users: list[dict]) -> None:
    # short way of writing a for loop that stops when it finds the first match.
    bob = next(u for u in seeded_users if u["name"] == "Bob")
    response = logged_in_admin.post("/user/create", json=bob)

    assert response.status_code == 409