import pytest
from connexion import App

@pytest.fixture
def app():
    app = App(__name__)

    @app.route("/test_get", methods=["GET"])
    def test_get(**kwargs):
        return kwargs.get('name', 'get')

    return app

def test_get_with_kwargs(app):
    app_client = app.test_client()
    response = app_client.get("/test_get?name=test")
    assert response.data.decode() == "test"

def test_get_without_kwargs(app):
    app_client = app.test_client()
    response = app_client.get("/test_get")
    assert response.data.decode() == "get"

def test_get_with_empty_kwargs(app):
    app_client = app.test_client()
    response = app_client.get("/test_get?name=")
    assert response.data.decode() == ""