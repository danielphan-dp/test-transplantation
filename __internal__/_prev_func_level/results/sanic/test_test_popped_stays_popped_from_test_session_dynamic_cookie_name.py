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

def test_get_method_with_params(app):
    request, response = app.test_client.get("/get", params=[("param1", "value1")])
    assert request.args.get("param1") == "value1"

def test_get_method_no_params(app):
    request, response = app.test_client.get("/get")
    assert request.args == {}

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_multiple_params(app):
    request, response = app.test_client.get("/get", params=[("param1", "value1"), ("param2", "value2")])
    assert request.args.get("param1") == "value1"
    assert request.args.get("param2") == "value2"