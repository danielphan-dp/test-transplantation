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

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get", params=[("param", "value")])
    assert response.text == "I am get method"
    assert response.status == 200
    assert request.args.get("param") == "value"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_empty_query(app):
    request, response = app.test_client.get("/get", params=[("empty", "")])
    assert response.text == "I am get method"
    assert response.status == 200
    assert request.args.get("empty") == ""