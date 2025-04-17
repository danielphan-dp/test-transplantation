import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_non_str_headers(app):
    @app.route("/get_with_headers")
    async def get_with_headers(request):
        headers = {"answer": 42}
        return text("Hello", headers=headers)

    request, response = app.test_client.get("/get_with_headers")
    assert response.headers.get("answer") == "42"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.route("/get_with_query")
    async def get_with_query(request):
        param = request.args.get("param", "default")
        return text(f"Query param is {param}")

    request, response = app.test_client.get("/get_with_query?param=test")
    assert response.text == "Query param is test"