import pytest
from connexion import App

@pytest.fixture
def app():
    app = App(__name__)
    return app

def test_get_with_kwargs(app):
    app_client = app.test_client()
    response = app_client.get("/v1.0/get?param1=value1&param2=value2")
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_without_kwargs(app):
    app_client = app.test_client()
    response = app_client.get("/v1.0/get")
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(app):
    app_client = app.test_client()
    response = app_client.get("/v1.0/get?param1=")
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'param1': ''}