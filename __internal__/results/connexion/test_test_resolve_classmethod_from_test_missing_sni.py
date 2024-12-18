import pytest

@pytest.fixture
def simple_app():
    from connexion import App
    app = App(__name__)
    return app

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/get", query_string={'key': 'value'})
    assert response.json == {'key': 'value', 'name': 'get'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/get")
    assert response.json == [{'name': 'get'}]

def test_get_with_multiple_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/get", query_string={'key1': 'value1', 'key2': 'value2'})
    assert response.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/get", query_string={})
    assert response.json == [{'name': 'get'}]