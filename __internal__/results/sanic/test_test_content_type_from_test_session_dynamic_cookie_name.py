import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    async def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_content_type(app):
    request, response = app.test_client.get("/get")
    assert request.content_type == "text/plain; charset=utf-8"
    assert response.content_type == "text/plain; charset=utf-8"

def test_get_method_with_custom_header(app):
    headers = {"Custom-Header": "CustomValue"}
    request, response = app.test_client.get("/get", headers=headers)
    assert request.headers.get("Custom-Header") == "CustomValue"
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.text == "I am get method"  # Ensure query params don't affect response
    assert request.args.get("param") == "value"