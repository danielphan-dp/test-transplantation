import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    async def get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_ssl(app):
    request, response = app.test_client.get("/get", server_kwargs={"ssl": True})
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_without_ssl(app):
    with pytest.raises(ValueError) as excinfo:
        app.test_client.get("/get", server_kwargs={"ssl": False})
    assert "Invalid ssl argument" in str(excinfo.value)