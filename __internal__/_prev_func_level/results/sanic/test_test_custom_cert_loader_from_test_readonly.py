import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    async def get_handler(request):
        return text("I am get method")

    return app

def test_get_method(app):
    client = SanicTestClient(app)

    request, response = client.get("/get")
    assert response.status_code == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    client = SanicTestClient(app)

    request, response = client.get("/invalid")
    assert response.status_code == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    client = SanicTestClient(app)

    request, response = client.get("/get?param=value")
    assert response.status_code == 200
    assert response.text == "I am get method"  # Ensure query params don't affect response

def test_get_method_with_headers(app):
    client = SanicTestClient(app)

    request, response = client.get("/get", headers={"Custom-Header": "value"})
    assert response.status_code == 200
    assert response.text == "I am get method"  # Ensure headers don't affect response

def test_get_method_with_ssl(app):
    class MyCertLoader:
        def load(self, app: Sanic):
            return app

    app.certloader_class = MyCertLoader

    client = SanicTestClient(app, port=44556)
    request, response = client.get("https://localhost:44556/get")
    assert request.scheme == "https"
    assert response.status_code == 200
    assert response.text == "I am get method"