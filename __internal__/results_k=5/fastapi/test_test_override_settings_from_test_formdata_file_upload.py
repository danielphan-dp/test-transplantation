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
    assert response.json()['msg'] == 'Hello World'

def test_app_empty_path():
    with client:
        response = client.get('/nonexistent')
    assert response.status_code == 404

def test_app_method_not_allowed():
    with client:
        response = client.post('/')
    assert response.status_code == 405

def test_app_query_param():
    with client:
        response = client.get('/?name=test')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello World'}  # Assuming the app handles query params in a specific way