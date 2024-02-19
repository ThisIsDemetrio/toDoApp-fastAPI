from config.get_context import get_context
import pytest
from fastapi.testclient import TestClient

from main import app
from tests.utils import clear_todo_collection, get_context_for_tests, get_todo_document_by_id, insert_documents_in_todo_collection, open_mock_file

client = TestClient(app)
app.dependency_overrides[get_context] = get_context_for_tests

@pytest.fixture(autouse=True)
def setup_on_each_test():
    toDoNotes = open_mock_file()
    insert_documents_in_todo_collection(toDoNotes)
    
    yield

    # After: we clear the "todo" collection
    clear_todo_collection()

def test_get_document_by_id():
    response = client.get("/note/10001")

    assert response.status_code == 200
    assert response.json()["id"] == "10001"
    assert response.json()["title"] == "Call the dentist"
    assert response.json()["category"] == "health"

def test_get_all():
    response = client.get("/note")

    assert response.status_code == 200
    assert len(response.json()) == 5

    response = client.get("/note?after=2021-11-17T00:00:00.000Z")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.get("/note?after=2021-11-06T00:00:00.000Z&before=2021-11-17T23:59:59.999Z")
    assert response.status_code == 200
    assert len(response.json()) == 4

    response = client.get("/note?after=1991-01-01T00:00:00.000Z&before=1991-12-31T23:59:59.999Z")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_add_document():
    note = {
        "id": "",
        "title": "Buy flowers",
        "description": "Roses or lilies",
        "completed": False,
        "dueDate": None,
        "remainders": [],
        "tags": [],
        "category": "gifts"
    }

    post_response = client.post("/note/", json=note)

    assert post_response.status_code == 200
    assert post_response.json()["status"] == "OK"
    note_id = post_response.json()["id"]
    assert note_id is not None


    new_doc = get_todo_document_by_id(note_id)
    assert new_doc is not None
    assert new_doc["id"] == note_id
    assert new_doc["title"] == "Buy flowers"
    assert new_doc["category"] == "gifts"
    assert new_doc["creationDate"] is not None

def test_update_document():
    updated_note = {
        "id": "10001",
        "creationDate": "2021-11-06T14:22:31.000Z",
        "title": "Call dentist Samir",
        "description": "Number 555-123-1230, get appointment asap",
        "completed": False,
        "dueDate": None,
        "remainders": [],
        "tags": ["dentist"],
        "category": "health"
    }

    patch_response = client.patch("/note/10001", json=updated_note)

    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == "OK"
    assert patch_response.json()["id"] == "10001"

    updated_doc = get_todo_document_by_id("10001")
    assert updated_doc is not None
    assert updated_doc["title"] == "Call dentist Samir"
    assert updated_doc["category"] == "health"

def test_set_to_complete():
    set_to_true_response = client.patch("/note/setToCompleted/10002")

    assert set_to_true_response.status_code == 200
    assert set_to_true_response.json()["status"] == "OK"

    updated_doc = get_todo_document_by_id("10002")
    assert updated_doc["completed"] is True

def test_set_to_not_complete():
    set_to_not_complete = client.patch("/note/setToNotCompleted/10003")

    assert set_to_not_complete.status_code == 200
    assert set_to_not_complete.json()["status"] == "OK"

    updated_doc = get_todo_document_by_id("10002")
    assert updated_doc["completed"] is False

def test_add_remainder():
    add_remainder = client.patch("/note/addRemainder/10001?new=2021-11-09T13:45:00.000Z")

    assert add_remainder.status_code == 200
    assert add_remainder.json()["status"] == "OK"

    updated_doc = get_todo_document_by_id("10001")
    assert updated_doc["remainders"] == ["2021-11-09T13:45:00.000Z"]


def test_remove_remainder():
    add_remainder = client.patch("/note/deleteRemainder/10002?old=2021-11-08T16:00:00.000Z")

    assert add_remainder.status_code == 200
    assert add_remainder.json()["status"] == "OK"

    updated_doc = get_todo_document_by_id("10002")
    assert updated_doc["remainders"] == []

def test_replace_remainder():
    add_remainder = client.patch("/note/updateRemainder/10004?old=2021-11-17T20:30:00.000Z&new=2021-11-17T20:45:00.000Z")

    assert add_remainder.status_code == 200
    assert add_remainder.json()["status"] == "OK"

    updated_doc = get_todo_document_by_id("10004")
    assert updated_doc["remainders"] == ["2021-11-17T20:00:00.000Z", "2021-11-17T20:45:00.000Z"]

def test_delete_document():
    delete_response = client.delete("/note/10001")

    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "OK"

    deleted_doc = get_todo_document_by_id("10001")
    assert deleted_doc is None
