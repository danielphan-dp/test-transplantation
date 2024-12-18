import pytest

@pytest.fixture
def simple_app():
    from connexion import FlaskApp
    app = FlaskApp(__name__)
    return app

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/test-get-endpoint?param1=value1&param2=value2")
    assert response.json == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/test-get-endpoint")
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/test-get-endpoint?param1=")
    assert response.json == {'name': 'get', 'param1': ''}