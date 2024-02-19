from config.get_context import get_context
import pytest
from fastapi.testclient import TestClient

from main import app
from tests.utils import clear_todo_collection, get_context_for_tests, get_todo_document_by_id, insert_documents_in_todo_collection, open_mock_file

client = TestClient(app)
app.dependency_overrides[get_context] = get_context_for_tests

@pytest.fixture(autouse=True)
def setup_on_each_test():
    # Before: we get the list of mock note documents to include in the "todo" collection
    toDoNotes = open_mock_file()
    insert_documents_in_todo_collection(toDoNotes)
    
    # During: we execute tests
    yield

    # After: we clear the "todo" collection
    clear_todo_collection()

def test_fail_to_get_document_by_id():
    res = client.get("/note/notadocument")

    assert res.status_code == 200
    assert res.json()["status"] == "KO"
    assert res.json()["code"] == "A01"
    assert res.json()["id"] == "notadocument"


def test_fail_to_patch_document():
    updated_note = {
        "id": "notadocument",
        "creationDate": "2021-11-08T14:27:51.000Z",
        "title": "Call dentist Samir",
        "description": "Number 555-123-1230, get appointment asap",
        "completed": False,
        "dueDate": None,
        "remainders": [],
        "tags": ["dentist"],
        "category": "health"
    }

    res = client.patch("/note/notadocument", json=updated_note)
    assert res.status_code == 200
    assert res.json()["status"] == "KO"
    assert res.json()["code"] == "A01"
    assert res.json()["id"] == "notadocument"

def test_fail_to_set_to_complete():
    res = client.patch("/note/setToCompleted/10003")

    assert res.status_code == 200
    assert res.json()["status"] == "KO"
    assert res.json()["code"] == "C01"

    updated_doc = get_todo_document_by_id("10003")
    assert updated_doc["completed"] is True

def test_fail_set_to_not_complete():
    res = client.patch("/note/setToNotCompleted/10002")

    assert res.status_code == 200
    assert res.json()["status"] == "KO"
    assert res.json()["code"] == "C02"

    updated_doc = get_todo_document_by_id("10002")
    assert updated_doc["completed"] is False

def test_fail_to_delete_document():
    res = client.delete("/note/notadocument")

    assert res.status_code == 200
    assert res.json()["status"] == "KO"
    assert res.json()["code"] == "A01"
    assert res.json()["id"] == "notadocument"
