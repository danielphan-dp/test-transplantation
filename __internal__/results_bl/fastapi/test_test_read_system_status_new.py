import pytest
from fastapi.testclient import TestClient
from utils.needs_py310 import needs_py310
from docs_src.security.tutorial005_an_py310.app import get_access_token

@needs_py310
def test_get_access_token_valid_credentials(client: TestClient):
    access_token = get_access_token(username='johndoe', password='secret', client=client)
    assert access_token is not None

@needs_py310
def test_get_access_token_invalid_credentials(client: TestClient):
    access_token = get_access_token(username='invaliduser', password='wrongpassword', client=client)
    assert access_token is None

@needs_py310
def test_get_access_token_with_scope(client: TestClient):
    access_token = get_access_token(username='johndoe', password='secret', scope='read', client=client)
    assert access_token is not None

@needs_py310
def test_get_access_token_no_username(client: TestClient):
    access_token = get_access_token(username='', password='secret', client=client)
    assert access_token is None

@needs_py310
def test_get_access_token_no_password(client: TestClient):
    access_token = get_access_token(username='johndoe', password='', client=client)
    assert access_token is None

@needs_py310
def test_get_access_token_no_credentials(client: TestClient):
    access_token = get_access_token(client=client)
    assert access_token is not None

@needs_py310
def test_get_access_token_invalid_scope(client: TestClient):
    access_token = get_access_token(username='johndoe', password='secret', scope='invalidscope', client=client)
    assert access_token is not None  # Assuming the API does not restrict access based on invalid scope.