import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get-method")
    async def get_method(request):
        return text("I am get method")

    return app

def test_get_method(app):
    client = SanicTestClient(app)

    request, response = client.get("/get-method")
    assert response.status_code == 200
    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    client = SanicTestClient(app)

    request, response = client.get("/get-method?param=value")
    assert response.status_code == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    client = SanicTestClient(app)

    request, response = client.get("/non-existent-path")
    assert response.status_code == 404
    assert "Requested URL /non-existent-path not found" in response.text

def test_get_method_with_invalid_method(app):
    client = SanicTestClient(app)

    request, response = client.post("/get-method")
    assert response.status_code == 405
    assert "Method POST not allowed for URL /get-method" in response.text