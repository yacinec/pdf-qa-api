import os
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_upload_invalid_extension():
    with open("tests/fake.txt", "w") as f:
        f.write("Not a PDF.")

    with open("tests/fake.txt", "rb") as f:
        response = client.post("/upload_pdf", files={"file": ("fake.txt", f, "text/plain")})

    os.remove("tests/fake.txt")
    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]

def test_upload_valid_pdf():
    with open("tests/sample.pdf", "rb") as f:
        response = client.post("/upload_pdf", files={"file": ("sample.pdf", f, "application/pdf")})
    assert response.status_code == 200
    assert "indexed successfully" in response.json()["message"]

def test_question_after_upload():
    response = client.get("/answer", params={"question": "Quel est le chiffre d'affaires 2024"})
    assert response.status_code == 200
    assert "answer" in response.json()