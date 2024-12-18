import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from docs_src.settings.app02.main import app

client = TestClient(app)

@pytest.fixture
def override_settings(monkeypatch):
    monkeypatch.setenv("ENV", "test")

def test_app_status_code():
    with client:
        response = client.get('/')
    assert response.status_code == 200

def test_app_content_type():
    with client:
        response = client.get('/')
    assert response.headers['content-type'] == 'application/json'

def test_app_response_structure():
    with client:
        response = client.get('/')
    assert 'msg' in response.json()

def test_app_empty_path():
    with client:
        response = client.get('/nonexistent')
    assert response.status_code == 404

def test_app_override_settings(override_settings):
    from docs_src.settings.app02 import test_main
    test_main.test_app()