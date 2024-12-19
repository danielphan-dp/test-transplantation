import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    test_client = SanicTestClient(app)
    request, response = test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_custom_header(app):
    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    test_client = SanicTestClient(app)
    request, response = test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_parameters(app):
    @app.get("/get")
    def get_handler(request):
        return text(f"Query param: {request.args.get('param', 'None')}")

    test_client = SanicTestClient(app)
    request, response = test_client.get("/get?param=test")
    assert response.text == "Query param: test"

def test_get_method_with_empty_response(app):
    @app.get("/get")
    def get_handler(request):
        return text("")

    test_client = SanicTestClient(app)
    request, response = test_client.get("/get")
    assert response.text == ""