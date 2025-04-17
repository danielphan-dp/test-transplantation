import pytest
from fastapi.testclient import TestClient
from docs_src.settings.app02.main import app

client = TestClient(app)

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

def test_app_response_message():
    with client:
        response = client.get('/')
    assert response.json() == {'msg': 'Hello World'}

def test_app_invalid_route():
    with client:
        response = client.get('/invalid-route')
    assert response.status_code == 404

def test_app_empty_query():
    with client:
        response = client.get('/?query=')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello World'}  # Assuming the app handles empty queries this way