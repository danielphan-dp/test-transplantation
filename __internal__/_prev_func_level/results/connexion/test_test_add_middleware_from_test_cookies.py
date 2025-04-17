import pytest
from connexion import FlaskApp

@pytest.fixture
def app():
    app = FlaskApp(__name__)
    return app

def test_get_with_kwargs(app):
    @app.route("/v1.0/get")
    def get_method(**kwargs):
        return get(**kwargs)

    app_client = app.test_client()
    response = app_client.get("/v1.0/get?param1=value1&param2=value2")
    assert response.json == {'param1': 'value1', 'param2': 'value2', 'name': 'get'}

def test_get_without_kwargs(app):
    @app.route("/v1.0/get")
    def get_method():
        return get()

    app_client = app.test_client()
    response = app_client.get("/v1.0/get")
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(app):
    @app.route("/v1.0/get")
    def get_method(**kwargs):
        return get(**kwargs)

    app_client = app.test_client()
    response = app_client.get("/v1.0/get?param1=")
    assert response.json == {'param1': '', 'name': 'get'}