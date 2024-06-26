import pytest
from fastapi.testclient import TestClient
from fastapi import status

from app.get_context import get_context
from app.responses.IdNotFoundResponse import IdNotFoundResponse
from main import app
from services.auth.utils import get_current_active_user
from tests.utils import (
    assert_ko,
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


def test_get_document_by_id():
    id = "10001"
    res = client.get(f"/todo/{id}")

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["result"]["id"] == id
    assert res.json()["result"]["title"] == "Call the dentist"
    assert res.json()["result"]["category"] == "health"


def test_fail_to_get_document_by_id():
    res = client.get("/todo/notadocument")

    assert res.status_code == status.HTTP_200_OK
    assert_ko(IdNotFoundResponse.internal_code, res)
    assert res.json()["id"] == "notadocument"


def test_fail_get_document_of_another_user():
    id = "10004"
    res = client.get(f"/todo/{id}")

    assert res.status_code == status.HTTP_200_OK
    assert_ko(IdNotFoundResponse.internal_code, res)
    assert res.json()["id"] == "10004"
