from app import error_handling
from app.ErrorCode import ErrorCode
from app.get_context import get_context
import pytest
from fastapi.testclient import TestClient

from main import app
from services.auth.utils import get_current_active_user
from tests.utils import assert_ko, clear_todo_collection, get_context_for_tests, get_current_user_for_tests, insert_documents_in_todo_collection, open_mock_file

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

def test_get_all():
    response = client.get("/todo")

    assert response.status_code == 200
    assert len(response.json()) == 5

    response = client.get("/todo?after=2021-11-17T00:00:00.000Z")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.get("/todo?after=2021-11-06T00:00:00.000Z&before=2021-11-17T23:59:59.999Z")
    assert response.status_code == 200
    assert len(response.json()) == 4

    response = client.get("/todo?after=1991-01-01T00:00:00.000Z&before=1991-12-31T23:59:59.999Z")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_fail_for_get_all_with_invalid_dates():
    assert_ko(ErrorCode.A02, client.get("/todo?before=2021-11-T16:0:00.000Z"))
    assert_ko(ErrorCode.A02, client.get("/todo?before=2021-11-03T16:00:00.000Z&after=202111-T16:00:00.000Z"))
