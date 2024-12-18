import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get_with_param")
    def get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "Received param: test"
    assert response.status == 200

def test_get_method_empty_response(app):
    @app.get("/get_empty")
    def get_empty(request):
        return text("")

    request, response = app.test_client.get("/get_empty")
    assert response.text == ""
    assert response.status == 200

def test_get_method_with_custom_context(app):
    class CustomContext:
        FOO = "foo"

    class CustomRequest:
        @staticmethod
        def make_context() -> CustomContext:
            return CustomContext()

    app.request_class = CustomRequest

    @app.get("/get_custom_ctx")
    async def handler(request: CustomRequest):
        return text(f"Context FOO: {request.make_context().FOO}")

    request, response = app.test_client.get("/get_custom_ctx")
    assert response.text == "Context FOO: foo"
    assert response.status == 200