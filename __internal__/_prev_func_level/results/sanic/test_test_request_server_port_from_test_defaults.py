import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_method")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get_method")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_custom_header(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get_method", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert request.headers.get("Custom-Header") == "value"

def test_get_method_invalid_route(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get_method?param=value")
    assert response.text == "I am get method"
    assert response.status == 200
    assert request.args.get("param") == "value"