import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    test_client = SanicTestClient(app)

    request, response = test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_invalid_method(app):
    test_client = SanicTestClient(app)

    request, response = test_client.post("/get")
    assert response.status == 405

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    def handler(request):
        name = request.args.get('name', 'World')
        return text(f"I am get method, {name}")

    test_client = SanicTestClient(app)

    request, response = test_client.get("/get_with_params?name=Test")
    assert response.text == "I am get method, Test"

def test_get_method_no_query_params(app):
    @app.get("/get_with_params")
    def handler(request):
        return text("I am get method, World")

    test_client = SanicTestClient(app)

    request, response = test_client.get("/get_with_params")
    assert response.text == "I am get method, World"