from app.get_context import get_context
from fastapi.testclient import TestClient

from main import app
from tests.utils import get_context_for_tests, get_todo_document_by_id

client = TestClient(app)
app.dependency_overrides[get_context] = get_context_for_tests

def test_add_document():
    todo = {
        "id": "",
        "title": "Buy flowers",
        "description": "Roses or lilies",
        "completed": False,
        "dueDate": None,
        "remainders": [],
        "tags": [],
        "category": "gifts"
    }

    post_response = client.post("/todo/", json=todo)

    assert post_response.status_code == 200
    assert post_response.json()["status"] == "OK"
    doc_id = post_response.json()["id"]
    assert doc_id is not None


    new_doc = get_todo_document_by_id(doc_id)
    assert new_doc is not None
    assert new_doc["id"] == doc_id
    assert new_doc["title"] == "Buy flowers"
    assert new_doc["category"] == "gifts"
    assert new_doc["creationDate"] is not None
