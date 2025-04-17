import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request: Request):
        return text('I am get method')

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_allowed(app):
    request, response = app.test_client.post("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {"GET"}

    request, response = app.test_client.put("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {"GET"}

    request, response = app.test_client.delete("/")
    assert response.status == 405
    assert set(response.headers["Allow"].split(", ")) == {"GET"}

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers.get("Custom-Header") is None  # Ensure custom header is not in response