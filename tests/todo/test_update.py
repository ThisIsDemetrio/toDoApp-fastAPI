import pytest
from fastapi.testclient import TestClient

from app.ErrorCode import ErrorCode
from app.get_context import get_context
from main import app
from services.auth.utils import get_current_active_user
from tests.utils import (
    assert_ko,
    clear_todo_collection,
    get_context_for_tests,
    get_current_user_for_tests,
    get_todo_document_by_id,
    insert_documents_in_todo_collection,
    open_mock_file,
)

client = TestClient(app)
app.dependency_overrides[get_context] = get_context_for_tests
app.dependency_overrides[get_current_active_user] = get_current_user_for_tests


@pytest.fixture(autouse=True)
def setup_on_each_test():
    # Safety check, we clean up the collection
    clear_todo_collection()

    # We add test files
    todos = open_mock_file()
    insert_documents_in_todo_collection(todos)

    # Run the test
    yield

    # After: we clear the "todo" collection
    clear_todo_collection()


def test_update_document():
    updated_todo = {
        "id": "10001",
        "creationDate": "2021-11-06T14:22:31.000Z",
        "title": "Call dentist Samir",
        "description": "Number 555-123-1230, get appointment asap",
        "completed": False,
        "dueDate": None,
        "remainders": [],
        "tags": ["dentist"],
        "category": "health",
    }

    patch_response = client.put("/todo/10001", json=updated_todo)

    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == "OK"
    assert patch_response.json()["result"] == "10001"

    updated_doc = get_todo_document_by_id("10001")
    assert updated_doc is not None
    assert updated_doc["title"] == "Call dentist Samir"
    assert updated_doc["category"] == "health"


def test_fail_to_update_document():
    updated_todo = {
        "id": "notadocument",
        "creationDate": "2021-11-08T14:27:51.000Z",
        "title": "Call dentist Samir",
        "description": "Number 555-123-1230, get appointment asap",
        "completed": False,
        "dueDate": None,
        "remainders": [],
        "tags": ["dentist"],
        "category": "health",
    }

    res = client.put("/todo/notadocument", json=updated_todo)

    assert_ko(ErrorCode.A01, res)
    assert res.json()["id"] == "notadocument"
