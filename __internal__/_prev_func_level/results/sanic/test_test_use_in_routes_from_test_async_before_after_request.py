import pytest
from sanic import Sanic
from sanic.text import text
from sanic.constants import HTTPMethod

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get", methods=[HTTPMethod.GET])
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    @app.route("/get_with_param", methods=[HTTPMethod.GET])
    def get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_empty_response(app):
    @app.route("/get_empty", methods=[HTTPMethod.GET])
    def get_empty(request):
        return text("")

    request, response = app.test_client.get("/get_empty")
    assert response.status == 200
    assert response.text == ""