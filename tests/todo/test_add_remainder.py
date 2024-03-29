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

def test_add_remainder():
    add_remainder = client.patch("/todo/addRemainder/10001?new=2021-11-09T13:45:00.000Z")

    assert add_remainder.status_code == 200
    assert add_remainder.json()["status"] == "OK"

    updated_doc = get_todo_document_by_id("10001")
    assert updated_doc["remainders"] == ["2021-11-09T13:45:00.000Z"]

def test_fail_for_invalid_dates_in_remainder_methods():
    assert_ko(error_handling.A02, client.patch("/todo/addRemainder/10002?new=2021-11-T16:0:00.000Z"))
