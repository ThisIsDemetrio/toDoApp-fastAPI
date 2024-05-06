from fastapi.testclient import TestClient
from fastapi import status

from app.get_context import get_context
from main import app
from services.auth.utils import get_current_active_user
from tests.utils import (
    get_context_for_tests,
    get_current_user_for_tests,
    get_todo_document_by_id,
)

client = TestClient(app)
app.dependency_overrides[get_context] = get_context_for_tests
app.dependency_overrides[get_current_active_user] = get_current_user_for_tests


def test_add_document():
    todo = {
        "id": "",
        "title": "Buy flowers",
        "description": "Roses or lilies",
        "completed": False,
        "dueDate": None,
        "remainders": [],
        "tags": [],
        "category": "gifts",
    }

    res = client.post("/todo/", json=todo)

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["status"] == "OK"
    doc_id = res.json()["result"]
    assert doc_id is not None

    new_doc = get_todo_document_by_id(doc_id)
    assert new_doc is not None
    assert new_doc["id"] == doc_id
    assert new_doc["title"] == "Buy flowers"
    assert new_doc["user"] == "py_user"
    assert new_doc["category"] == "gifts"
    assert new_doc["creationDate"] is not None
