import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request):
        return text("I am get method")

    return app

def test_get_method(json_app):
    request, response = json_app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"
    assert "Content-Length" in response.headers
    assert response.headers["Content-Length"] == str(len(response.text))
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"

def test_get_method_with_invalid_route(json_app):
    request, response = json_app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(json_app):
    request, response = json_app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the method does not change based on query params

def test_get_method_with_headers(json_app):
    request, response = json_app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers["Custom-Header"] != "value"  # Custom headers should not affect the response

def test_get_method_empty_body(json_app):
    request, response = json_app.test_client.get("/", data="")
    assert response.status == 200
    assert response.text == "I am get method"  # Ensure the method handles empty body correctly