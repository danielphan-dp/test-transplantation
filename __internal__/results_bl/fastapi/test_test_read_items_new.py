import pytest
from fastapi.testclient import TestClient
from utils.needs_py310 import needs_py310
from docs_src.security.tutorial005_an_py310.app import get_access_token

@needs_py310
def test_get_access_token_no_scope(client: TestClient):
    access_token = get_access_token(client=client)
    assert access_token is not None

@needs_py310
def test_get_access_token_with_scope(client: TestClient):
    access_token = get_access_token(scope="read", client=client)
    assert access_token is not None

@needs_py310
def test_get_access_token_invalid_credentials(client: TestClient):
    access_token = get_access_token(username="invalid", password="wrong", client=client)
    assert access_token is None

@needs_py310
def test_get_access_token_empty_username(client: TestClient):
    access_token = get_access_token(username="", client=client)
    assert access_token is None

@needs_py310
def test_get_access_token_empty_password(client: TestClient):
    access_token = get_access_token(password="", client=client)
    assert access_token is None

@needs_py310
def test_get_access_token_no_credentials(client: TestClient):
    access_token = get_access_token(client=client)
    assert access_token is not None

@needs_py310
def test_get_access_token_scope_none(client: TestClient):
    access_token = get_access_token(scope=None, client=client)
    assert access_token is not None

@needs_py310
def test_get_access_token_invalid_scope(client: TestClient):
    access_token = get_access_token(scope="invalid_scope", client=client)
    assert access_token is None