import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.route("/get")
    def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get")
    def get_handler(request):
        param_value = request.args.get("param", "default")
        return text(f"Param is: {param_value}")

    request, response = app.test_client.get("/get?param=test")
    assert response.text == "Param is: test"

def test_get_method_with_no_query_params(app):
    @app.route("/get")
    def get_handler(request):
        return text("No params provided")

    request, response = app.test_client.get("/get")
    assert response.text == "No params provided"