import pytest
from fastapi.testclient import TestClient
from fastapi import status

from app.get_context import get_context
from main import app
from tests.auth.utils import (
    clear_users_collection,
    insert_documents_in_users_collection,
    open_mock_file,
)
from tests.utils import get_context_for_tests

client = TestClient(app)
app.dependency_overrides[get_context] = get_context_for_tests


@pytest.fixture(autouse=True)
def setup_on_each_test():
    # Safety check, we clean up the collection
    clear_users_collection()

    # We add test files
    users = open_mock_file()
    insert_documents_in_users_collection(users)

    # Run the test
    yield

    # After: we clear the "todo" collection
    clear_users_collection()


def test_login():
    form_data = {"username": "john", "password": "secret"}
    response = client.post("/login", data=form_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] is not None
