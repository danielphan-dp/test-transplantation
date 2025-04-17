import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    app.config.KEEP_ALIVE_TIMEOUT = 1

    @app.get("/")
    async def base_handler(request):
        return text("111122223333444455556666777788889999")

    @app.get("/get_method")
    async def get_method_handler(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get_method")
    assert response.status == 200
    assert response.text == "I am get method"

def test_base_handler(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "111122223333444455556666777788889999"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent")
    assert response.status == 404
    assert "Requested URL /non_existent not found" in response.text

def test_get_method_with_invalid_method(app):
    request, response = app.test_client.post("/get_method")
    assert response.status == 405
    assert "Method POST not allowed for URL /get_method" in response.text