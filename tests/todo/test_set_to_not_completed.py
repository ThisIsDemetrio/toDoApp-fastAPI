import pytest
from app import error_handling
from app.get_context import get_context
from fastapi.testclient import TestClient

from main import app
from tests.utils import assert_ko, clear_todo_collection, get_context_for_tests, get_todo_document_by_id, insert_documents_in_todo_collection, open_mock_file

client = TestClient(app)
app.dependency_overrides[get_context] = get_context_for_tests

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

def test_set_to_not_complete():
    set_to_not_complete = client.patch("/todo/setToNotCompleted/10003")

    assert set_to_not_complete.status_code == 200
    assert set_to_not_complete.json()["status"] == "OK"

    updated_doc = get_todo_document_by_id("10002")
    assert updated_doc["completed"] is False

def test_fail_set_to_not_complete_if_not_completed_yet():
    res = client.patch("/todo/setToNotCompleted/10002")

    assert_ko(error_handling.C02, res)

    updated_doc = get_todo_document_by_id("10002")
    assert updated_doc["completed"] is False
