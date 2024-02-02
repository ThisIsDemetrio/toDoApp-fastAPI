from config.get_context import get_context
import pytest
from fastapi.testclient import TestClient

from main import app
from tests.utils import clear_todo_collection, get_context_for_tests

client = TestClient(app)

app.dependency_overrides[get_context] = get_context_for_tests

@pytest.fixture(autouse=True)
def setup_on_each_test():
    # No operations before
    yield
    # After: we clear the "todo" collection
    clear_todo_collection()

def test_execute_full_cycle():
    note_id = ""
    # We have the following document. We save it, we retrieve it, we update it, then we delete it
    note_title = "Call the dentist"
    note = {
        "id": note_id,
        "title": note_title,
        "description": "Number 555-123-1230, get appointment asap",
        "completed": False,
        "dueDate": None,
        "remainders": [],
        "tags": ["dentist"],
        "category": "health"
    }

    # POST / 
    post_response = client.post("/note/", json=note)

    assert post_response.status_code == 200
    assert post_response.json()["status"] == "OK"
    note_id = post_response.json()["id"]
    assert note_id is not None

    # GET /<id>
    get_response = client.get(f"/note/{note_id}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == note_id
    assert get_response.json()["title"] == note_title

    # PATCH /<id>
    updated_note_title = "Call dentist Samir"
    updated_note = {
        "id": note_id,
        "title": updated_note_title,
        "description": "Number 555-123-1230, get appointment asap",
        "completed": False,
        "dueDate": None,
        "remainders": [],
        "tags": ["dentist"],
        "category": "health"
    }

    patch_response = client.patch(f"/note/{note_id}", json=updated_note)

    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == "OK"
    assert patch_response.json()["id"] == note_id

    # GET /<id> (to fetch the updated note)
    get_on_updated_note_response = client.get(f"/note/{note_id}")

    assert get_on_updated_note_response.status_code == 200
    assert get_on_updated_note_response.json()["id"] == note_id
    assert get_on_updated_note_response.json()["title"] == updated_note_title

    # DELETE /<id>
    delete_response = client.delete(f"/note/{note_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "OK"



