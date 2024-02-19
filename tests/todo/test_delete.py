from app import error_handling
from app.get_context import get_context
import pytest
from fastapi.testclient import TestClient

from main import app
from tests.utils import assert_ko, clear_todo_collection, get_context_for_tests, get_todo_document_by_id, insert_documents_in_todo_collection, open_mock_file

client = TestClient(app)
app.dependency_overrides[get_context] = get_context_for_tests

@pytest.fixture(autouse=True)
def setup_on_each_test():
    todos = open_mock_file()
    insert_documents_in_todo_collection(todos)
    
    yield

    # After: we clear the "todo" collection
    clear_todo_collection()

def test_delete_document():
    delete_response = client.delete("/todo/10001")

    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "OK"

    deleted_doc = get_todo_document_by_id("10001")
    assert deleted_doc is None

def test_fail_to_delete_non_existing_document():
    res = client.delete("/todo/notadocument")

    assert_ko(error_handling.A01, res)
    assert res.json()["id"] == "notadocument"
