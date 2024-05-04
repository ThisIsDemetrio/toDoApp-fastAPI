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
    todos = open_mock_file()
    insert_documents_in_todo_collection(todos)

    yield

    # After: we clear the "todo" collection
    clear_todo_collection()


def test_delete_document():
    id = "10001"
    res = client.delete(f"/todo/{id}")

    assert res.status_code == 200
    assert res.json()["status"] == "OK"

    deleted_doc = get_todo_document_by_id(id)
    assert deleted_doc is None


def test_fail_to_delete_non_existing_document():
    id = "not-a-document"
    res = client.delete(f"/todo/{id}")

    assert_ko(ErrorCode.A01, res)
    assert res.json()["id"] == id


def test_fail_delete_todo_of_another_user():
    id = "10004"
    res = client.delete(f"/todo/{id}")

    assert_ko(ErrorCode.A01, res)
