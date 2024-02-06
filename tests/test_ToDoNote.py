import os
from config import Client
from config.get_context import get_context
import json
import pytest
from fastapi.testclient import TestClient

from main import app
from tests.utils import clear_todo_collection, get_context_for_tests, get_todo_document_by_id, insert_documents_in_todo_collection

client = TestClient(app)
app.dependency_overrides[get_context] = get_context_for_tests

NOTE_MOCKS_RELATIVE_PATH = 'tests/documents.json'

@pytest.fixture(autouse=True)
def setup_on_each_test():
    # We open the document.json file and we retrieve the documents to be inserted in the DB
    print('Preparing environment for tests')
    file_path = os.path.join(os.getcwd(), NOTE_MOCKS_RELATIVE_PATH)
    with open(file_path, 'r') as json_file:
        toDoNotes = json.load(json_file)

    insert_documents_in_todo_collection(toDoNotes)
    
    yield

    # After: we clear the "todo" collection
    clear_todo_collection()

def test_get_document_by_id():
    get_response = client.get("/note/10001")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == "10001"
    assert get_response.json()["title"] == "Call the dentist"
    assert get_response.json()["category"] == "health"

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

    # POST / 
    post_response = client.post("/note/", json=note)

    assert post_response.status_code == 200
    assert post_response.json()["status"] == "OK"
    note_id = post_response.json()["id"]
    assert note_id is not None

    new_doc = get_todo_document_by_id(note_id)
    assert new_doc is not None
    assert new_doc["title"] == "Buy flowers"
    assert new_doc["category"] == "gifts"

def test_update_document():
    updated_note = {
        "id": "10001",
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

    new_doc = get_todo_document_by_id("10001")
    assert new_doc is not None
    assert new_doc["title"] == "Call dentist Samir"
    assert new_doc["category"] == "health"

def test_delete_document():
    delete_response = client.delete("/note/10001")

    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "OK"

    new_doc = get_todo_document_by_id("10001")
    assert new_doc is None
