import unittest
from uuid import uuid4

from fastapi.testclient import TestClient

from main import app


class ExceptionHandlingTests(unittest.TestCase):
    def setUp(self)->None:
        self.client = TestClient(app)
        self.email = f"user-{uuid4().hex}@example.com"
        self.payload = {
            "name": "Test User",
            "email": self.email,
            "password": "secret123",
            "age": 25,
            "gender": "male",
        }

    def test_register_returns_created_user_payload(self)->None:
        response = self.client.post("/auth/register", json=self.payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], 201)
        self.assertEqual(response.json()["message"], "user registered successfully")
        self.assertEqual(response.json()["data"]["email"], self.payload["email"])
        self.assertEqual(response.json()["data"]["name"], self.payload["name"])

    def test_duplicate_email_returns_global_error_payload(self)->None:
        self.client.post("/auth/register", json=self.payload)

        response = self.client.post("/auth/register", json=self.payload)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.json(),
            {"status_code": 409, "detail": "Email already registered"},
        )

    def test_wrong_password_returns_global_error_payload(self)->None:
        self.client.post("/auth/register", json=self.payload)

        response = self.client.post(
            "/auth/login",
            json={"email": self.payload["email"], "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"status_code": 401, "detail": "Password does not match"},
        )


if __name__ == "__main__":
    unittest.main()
