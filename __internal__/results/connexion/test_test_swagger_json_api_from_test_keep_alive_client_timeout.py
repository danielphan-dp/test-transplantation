import pytest
from connexion import App

@pytest.fixture
def app(simple_api_spec_dir, spec):
    app = App(__name__, specification_dir=simple_api_spec_dir)
    app.add_api(spec)
    return app

def test_get_with_kwargs(app):
    app_client = app.test_client()
    response = app_client.get('/v1.0/test_endpoint?param1=value1&param2=value2')
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_without_kwargs(app):
    app_client = app.test_client()
    response = app_client.get('/v1.0/test_endpoint')
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(app):
    app_client = app.test_client()
    response = app_client.get('/v1.0/test_endpoint?param1=')
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'param1': ''}