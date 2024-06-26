from typing import Literal
import pytest
from fastapi.testclient import TestClient
from fastapi import status

from app.responses.InvalidDateBadRequest import InvalidDateBadRequest
from app.get_context import get_context
from main import app
from services.auth.utils import get_current_active_user
from tests.utils import (
    clear_todo_collection,
    get_context_for_tests,
    get_current_user_for_tests,
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


@pytest.mark.parametrize(
    "expected_count, before, after, completed, limit",
    [
        # Simple case
        (7, None, None, None, None),
        # With before/after
        (4, None, "2021-11-17T00:00:00.000Z", None, None),
        (3, "2021-11-16T23:59:59.999Z", "2021-11-06T00:00:00.000Z", None, None),
        (0, "1991-01-01T00:00:00.000Z", "1991-12-31T23:59:59.999Z", None, None),
        # With completed
        (2, None, None, True, None),
        (5, None, None, False, None),
        (1, "2021-11-16T23:59:59.999Z", "2021-11-06T00:00:00.000Z", True, None),
        (2, "2021-11-16T23:59:59.999Z", "2021-11-06T00:00:00.000Z", False, None),
        # With limit
        (2, None, None, None, 2),
        (1, "2021-11-16T23:59:59.999Z", "2021-11-06T00:00:00.000Z", None, 1),
    ],
)
def test_get_all(expected_count, before, after, completed, limit):
    url = "/todo"
    if before is not None:
        url = "?".join([url, f"before={before}"])
    if after is not None:
        url = ("?" if before is None else "&").join([url, f"after={after}"])
    if completed is not None:
        url = ("?" if before is None else "&").join([url, f"completed={"true" if completed else "false"}"])
    if limit is not None:
        url = ("?" if before is None else "&").join([url, f"limit={limit}"])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["status"] == "OK"
    assert len(res.json()["result"]) == expected_count


@pytest.mark.parametrize(
    "before,after,invalidKey",
    [
        ("2021-11-T16:0:00.000Z", None, "before"),
        ("2021-11-03T16:00:00.000Z", "202111-T16:00:00.000Z", "after"),
    ],
)
def test_fail_for_get_all_with_invalid_dates(
    before: str, after: str, invalidKey: Literal["before", "after"]
):
    url = "/todo"
    if before is not None:
        url = "?".join([url, f"before={before}"])
    if after is not None:
        url = ("?" if before is None else "&").join([url, f"after={after}"])

    res = client.get(url)
    assert res.status_code == 400
    assert res.json()["detail"] == InvalidDateBadRequest.detail_message
    assert res.json()["key"] == invalidKey
    assert res.json()["value"] == after if invalidKey == "after" else before


@pytest.mark.parametrize("limit", [0, -1, 1.5, "alfa", True])
def test_fail_if_limit_is_negative(limit: str):
    url = f"/todo?limit={limit}"
    res = client.get(url)

    assert res.status_code == 400
    assert res.json()["detail"] == "limitNotValid"
    
