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

def test_get_method(app):
    test_client = SanicTestClient(app)

    request, response = test_client.get("/get")
    assert response.text == "I am get method"

def test_post_method_not_allowed(app):
    test_client = SanicTestClient(app)

    request, response = test_client.post("/get")
    assert response.status == 405

def test_get_method_with_query_params(app):
    test_client = SanicTestClient(app)

    request, response = test_client.get("/get?param=value")
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    test_client = SanicTestClient(app)

    request, response = test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_with_headers(app):
    test_client = SanicTestClient(app)

    headers = {"Custom-Header": "value"}
    request, response = test_client.get("/get", headers=headers)
    assert response.text == "I am get method"