import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.route("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.route("/get")
    def handler(request):
        name = request.args.get("name", "World")
        return text(f"I am get method, {name}")

    request, response = app.test_client.get("/get?name=Test")
    assert response.text == "I am get method, Test"
    assert response.status == 200

def test_get_method_with_no_query_params(app):
    @app.route("/get")
    def handler(request):
        return text("I am get method, World")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method, World"
    assert response.status == 200