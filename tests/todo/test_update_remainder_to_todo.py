from typing import Literal
import pytest
from fastapi.testclient import TestClient

from app.ErrorCode import ErrorCode
from app.errors.InvalidDateBadRequest import InvalidDateBadRequest
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


def test_update_remainder():
    id = "10006"
    old_remainder = "2021-11-17T20:30:00.000Z"
    new_remainder = "2021-11-17T20:45:00.000Z"

    res = client.patch(
        f"/todo/updateRemainder/{id}?old={old_remainder}&new={new_remainder}"
    )

    assert res.status_code == 200
    assert res.json()["status"] == "OK"

    updated_doc = get_todo_document_by_id(id)
    assert updated_doc["remainders"] == [
        "2021-11-17T20:00:00.000Z",
        "2021-11-17T20:45:00.000Z",
    ]


@pytest.mark.parametrize(
    "id,old,new,invalidKey",
    [
        ("10002", "2021-11-17T:30:00.000Z", "2021-11-17T20:45:00.000Z", "old"),
        ("10002", "2021-11-17T20:30:00.000Z", "202-117T20:45:00.000Z", "new"),
    ],
)
def test_fail_for_invalid_dates_in_remainder_methods(
    id: str, old: str, new: str, invalidKey: Literal["new", "old"]
):
    url = f"/todo/updateRemainder/{id}"
    if old is not None:
        url = "?".join([url, f"old={old}"])
    if new is not None:
        url = ("?" if old is None else "&").join([url, f"new={new}"])

    res = client.patch(url)
    assert res.status_code == 400
    assert res.json()["detail"] == InvalidDateBadRequest.detail_message
    assert res.json()["key"] == invalidKey
    assert res.json()["value"] == new if invalidKey == "new" else old


def test_fail_to_set_to_not_complete_another_user_todo():
    id = "10004"
    old_remainder = "2021-11-17T20:30:00.000Z"
    new_remainder = "2021-11-17T20:45:00.000Z"

    res = client.patch(
        f"/todo/updateRemainder/{id}?old={old_remainder}&new={new_remainder}"
    )

    assert_ko(ErrorCode.A01, res)
