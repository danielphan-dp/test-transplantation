import pytest
from fastapi.testclient import TestClient
from docs_src.settings.app02.main import app

client = TestClient(app)

@pytest.mark.needs_pydanticv2
def test_app_with_different_paths():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello World'}
    assert response.headers['content-type'] == 'application/json'

    response = client.get('/nonexistent-path')
    assert response.status_code == 404

    response = client.get('/?query=parameter')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello World'}

    response = client.get('/?another_query=parameter')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello World'}

    response = client.get('/?error_case=invalid')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello World'}