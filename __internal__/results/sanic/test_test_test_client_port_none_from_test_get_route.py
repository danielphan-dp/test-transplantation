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
    assert response.status == 200

def test_get_method_not_found(app):
    test_client = SanicTestClient(app)

    request, response = test_client.get("/nonexistent")
    assert response.status == 404

def test_post_method_not_allowed(app):
    test_client = SanicTestClient(app)

    request, response = test_client.post("/get")
    assert response.status == 405

def test_get_method_with_query_param(app):
    @app.get("/get")
    def handler_with_param(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    test_client = SanicTestClient(app)

    request, response = test_client.get("/get?param=test")
    assert response.text == "I am get method with param: test"
    assert response.status == 200

def test_get_method_empty_query_param(app):
    @app.get("/get")
    def handler_with_empty_param(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    test_client = SanicTestClient(app)

    request, response = test_client.get("/get?param=")
    assert response.text == "I am get method with param: "
    assert response.status == 200