import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.body == b"I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert b"Requested URL /invalid not found" in response.body

def test_get_method_with_query_params(app):
    @app.route("/query")
    def get_with_query(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/query?param=test")
    assert response.status == 200
    assert response.body == b"Received param: test"

def test_get_method_no_query_params(app):
    request, response = app.test_client.get("/query")
    assert response.status == 200
    assert response.body == b"Received param: default"