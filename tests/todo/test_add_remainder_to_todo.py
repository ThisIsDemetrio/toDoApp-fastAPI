import pytest
from fastapi.testclient import TestClient
from fastapi import status

from app.responses.IdNotFoundResponse import IdNotFoundResponse
from app.responses.InvalidDateBadRequest import InvalidDateBadRequest
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


def test_add_remainder():
    id = "10001"
    remainder = "2021-11-09T13:45:00.000Z"
    res = client.patch(f"/todo/addRemainder/{id}?new={remainder}")

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["status"] == "OK"

    updated_doc = get_todo_document_by_id(id)
    assert updated_doc["remainders"] == [remainder]


def test_fail_for_invalid_dates_in_remainder_methods():
    id = "10002"
    new = "2021-11-T16:0:00.000Z"
    res = client.patch(f"/todo/addRemainder/{id}?new={new}")
    assert res.status_code == 400
    assert res.json()["detail"] == InvalidDateBadRequest.detail_message
    assert res.json()["key"] == "new"
    assert res.json()["value"] == new


def test_fail_add_remainder_to_another_user_todo():
    id = "10004"
    remainder = "2021-11-09T13:45:00.000Z"
    res = client.patch(f"/todo/addRemainder/{id}?new={remainder}")

    assert_ko(IdNotFoundResponse.internal_code, res)
