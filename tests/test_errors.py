import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app, raise_server_exceptions=False)

def test_custom_exception_a():
    response = client.get("/test/a/-5")
    assert response.status_code == 409
    data = response.json()
    assert data["error_type"] == "CustomAError"
    assert "Value cannot be negative" in data["message"]

def test_custom_exception_b():
    response = client.get("/test/b/200")
    assert response.status_code == 404
    data = response.json()
    assert data["error_type"] == "CustomBError"
    assert "not found" in data["message"]

def test_validation_error():
    invalid_data = {
        "username": "a",
        "age": 17,
        "email": "notanemail",
        "password": "short"
    }
    response = client.post("/users/register", json=invalid_data)
    assert response.status_code == 422
    data = response.json()
    assert data["title"] == "Validation Error"
    assert len(data["errors"]) >= 1

def test_password_validation():
    invalid_pwd = {
        "username": "alice",
        "age": 25,
        "email": "alice@example.com",
        "password": "short",
        "phone": "+7999"
    }
    response = client.post("/users/register", json=invalid_pwd)
    assert response.status_code == 422
    data = response.json()
    assert any(e["field"] == "body.password" for e in data["errors"])

def test_unexpected_exception():
    response = client.get("/test/boom")
    # Теперь ожидаем 500, а не исключение
    assert response.status_code == 500
    data = response.json()
    assert data["error_type"] == "InternalServerError"

def test_log_file_exists():
    assert os.path.isfile("app.log")

def test_log_contains_error():
    with open("app.log", "r", encoding="utf-8") as f:
        content = f.read()
    assert "ERROR" in content
