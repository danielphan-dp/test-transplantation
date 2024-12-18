import pytest
from connexion import App

@pytest.fixture
def app():
    app = App(__name__)

    @app.route("/test_get", methods=["GET"])
    def test_get(**kwargs):
        if kwargs:
            kwargs.update({'name': 'get'})
            return kwargs
        else:
            return [{'name': 'get'}]

    return app

def test_get_with_kwargs(app):
    app_client = app.test_client()
    response = app_client.get("/test_get?param1=value1&param2=value2")
    assert response.json == {'param1': 'value1', 'param2': 'value2', 'name': 'get'}

def test_get_without_kwargs(app):
    app_client = app.test_client()
    response = app_client.get("/test_get")
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(app):
    app_client = app.test_client()
    response = app_client.get("/test_get?param1=")
    assert response.json == {'param1': '', 'name': 'get'}

def test_get_with_multiple_params(app):
    app_client = app.test_client()
    response = app_client.get("/test_get?param1=value1&param2=value2&param3=value3")
    assert response.json == {'param1': 'value1', 'param2': 'value2', 'param3': 'value3', 'name': 'get'}