import pytest
from connexion import App

@pytest.fixture
def app():
    app = App(__name__)
    return app

def test_get_method_no_kwargs(app):
    app.add_url_rule("/get", "get", lambda: [{'name': 'get'}], methods=["GET"])
    client = app.test_client()
    response = client.get("/get")
    assert response.json == [{'name': 'get'}]

def test_get_method_with_kwargs(app):
    app.add_url_rule("/get", "get", lambda **kwargs: kwargs, methods=["GET"])
    client = app.test_client()
    response = client.get("/get?key=value")
    assert response.json == {'key': 'value', 'name': 'get'}

def test_get_method_with_multiple_kwargs(app):
    app.add_url_rule("/get", "get", lambda **kwargs: kwargs, methods=["GET"])
    client = app.test_client()
    response = client.get("/get?key1=value1&key2=value2")
    assert response.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_method_with_no_query_params(app):
    app.add_url_rule("/get", "get", lambda **kwargs: kwargs, methods=["GET"])
    client = app.test_client()
    response = client.get("/get")
    assert response.json == {'name': 'get'}

def test_get_method_with_empty_kwargs(app):
    app.add_url_rule("/get", "get", lambda **kwargs: kwargs, methods=["GET"])
    client = app.test_client()
    response = client.get("/get?empty=")
    assert response.json == {'empty': '', 'name': 'get'}