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
    # Safety check, we clean up the collection
    clear_todo_collection()

    # We add test files
    todos = open_mock_file()
    insert_documents_in_todo_collection(todos)
    
    # Run the test
    yield

    # After: we clear the "todo" collection
    clear_todo_collection()

def test_get_document_by_id():
    response = client.get("/todo/10001")

    assert response.status_code == 200
    assert response.json()["id"] == "10001"
    assert response.json()["title"] == "Call the dentist"
    assert response.json()["category"] == "health"

def test_fail_to_get_document_by_id():
    res = client.get("/todo/notadocument")

    assert res.status_code == 200
    assert_ko(error_handling.A01, res)
    assert res.json()["id"] == "notadocument"
