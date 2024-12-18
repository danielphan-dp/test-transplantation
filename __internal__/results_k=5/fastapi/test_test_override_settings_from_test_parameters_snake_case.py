import pytest
from fastapi.testclient import TestClient
from docs_src.settings.app02.main import app

client = TestClient(app)

@pytest.mark.needs_pydanticv2
def test_app_with_different_paths():
    response = client.get('/')
    assert response.json() == {'msg': 'Hello World'}
    assert response.headers['content-type'] == 'application/json'

    # Test additional paths
    response = client.get('/nonexistent-path')
    assert response.status_code == 404

    response = client.get('/another-path')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Another Response'}

    # Test with query parameters
    response = client.get('/?param=value')
    assert response.status_code == 200
    assert response.json() == {'msg': 'Hello World', 'param': 'value'}

    # Test with invalid query parameters
    response = client.get('/?invalid_param=value')
    assert response.status_code == 400
    assert 'detail' in response.json()