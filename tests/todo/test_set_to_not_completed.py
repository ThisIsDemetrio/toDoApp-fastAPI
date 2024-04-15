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


def test_set_to_not_complete():
    id = "10003"
    res = client.patch(f"/todo/setToNotCompleted/{id}")

    assert res.status_code == 200
    assert res.json()["status"] == "OK"

    updated_doc = get_todo_document_by_id(id)
    assert updated_doc["completed"] is False


def test_fail_set_to_not_complete_if_not_completed_yet():
    id = "10002"
    res = client.patch(f"/todo/setToNotCompleted/{id}")

    assert_ko(ErrorCode.C02, res)

    updated_doc = get_todo_document_by_id(id)
    assert updated_doc["completed"] is False


def test_fail_to_set_to_not_complete_another_user_note():
    id = "10004"
    res = client.patch(f"/todo/setToNotCompleted/{id}")

    assert_ko(ErrorCode.C02, res)

    updated_doc = get_todo_document_by_id(id)
    assert updated_doc["completed"] is False
