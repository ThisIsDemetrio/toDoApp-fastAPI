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
    id = "10001"

    updated_todo = {
        "id": id,
        "creationDate": "2021-11-06T14:22:31.000Z",
        "user": "py_user",
        "title": "Call dentist Samir",
        "description": "Number 555-123-1230, get appointment asap",
        "completed": False,
        "dueDate": None,
        "remainders": [],
        "tags": ["dentist"],
        "category": "health",
    }

    res = client.put(f"/todo/{id}", json=updated_todo)

    assert res.status_code == 200
    assert res.json()["status"] == "OK"
    assert res.json()["result"] == id

    updated_doc = get_todo_document_by_id(id)
    assert updated_doc is not None
    assert updated_doc["title"] == "Call dentist Samir"
    assert updated_doc["user"] == "py_user"
    assert updated_doc["category"] == "health"


def test_fail_to_update_document():
    id = "notadocument"

    updated_todo = {
        "id": id,
        "creationDate": "2021-11-08T14:27:51.000Z",
        "user": "py_user",
        "title": "Call dentist Samir",
        "description": "Number 555-123-1230, get appointment asap",
        "completed": False,
        "dueDate": None,
        "remainders": [],
        "tags": ["dentist"],
        "category": "health",
    }

    res = client.put(f"/todo/{id}", json=updated_todo)

    assert_ko(ErrorCode.A01, res)
    assert res.json()["id"] == id


def test_fail_to_update_document_of_another_user():
    id = "10004"

    updated_todo = {
        "id": id,
        "creationDate": "2021-11-17T15:00:00.000Z",
        "user": "not_a_py_user",
        "title": "Call an ambulance",
        "description": "but not for me!",
        "completed": False,
        "dueDate": None,
        "remainders": [],
        "tags": ["jokes"],
        "category": "self",
    }

    res = client.put(f"/todo/{id}", json=updated_todo)

    assert res.status_code == 403
