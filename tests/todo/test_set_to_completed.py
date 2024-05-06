import pytest
from fastapi.testclient import TestClient
from fastapi import status

from app.get_context import get_context
from app.responses.AlreadyCompletedResponse import AlreadyCompletedResponse
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


def test_set_to_complete():
    id = "10002"
    set_to_true_response = client.patch(f"/todo/setToCompleted/{id}")

    assert set_to_true_response.status_code == status.HTTP_200_OK
    assert set_to_true_response.json()["status"] == "OK"

    updated_doc = get_todo_document_by_id(id)
    assert updated_doc["completed"] is True


def test_fail_to_set_to_complete_if_already_completed():
    id = "10003"
    res = client.patch(f"/todo/setToCompleted/{id}")

    assert_ko(AlreadyCompletedResponse.internal_code, res)

    updated_doc = get_todo_document_by_id(id)
    assert updated_doc["completed"] is True


def test_fail_to_set_to_complete_another_user_todo():
    id = "10008"
    res = client.patch(f"/todo/setToCompleted/{id}")

    assert_ko(AlreadyCompletedResponse.internal_code, res)

    updated_doc = get_todo_document_by_id(id)
    assert updated_doc["completed"] is True
