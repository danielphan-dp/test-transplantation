import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    async def get_handler(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.body == b"I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get_with_params")
    async def get_with_params(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.body == b"Received param: test"

def test_get_method_empty_query_params(app):
    request, response = app.test_client.get("/get_with_params")
    assert response.body == b"Received param: default"