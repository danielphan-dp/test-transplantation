import pytest
from connexion import App

@pytest.fixture
def app():
    app = App(__name__)
    return app

def test_get_with_kwargs(app):
    app.add_api('path/to/openapi.yaml')
    client = app.test_client()
    response = client.get('/v1.0/resource', query_string={'key': 'value'})
    assert response.status_code == 200
    assert response.json == {'key': 'value', 'name': 'get'}

def test_get_without_kwargs(app):
    app.add_api('path/to/openapi.yaml')
    client = app.test_client()
    response = client.get('/v1.0/resource')
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(app):
    app.add_api('path/to/openapi.yaml')
    client = app.test_client()
    response = client.get('/v1.0/resource', query_string={})
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]