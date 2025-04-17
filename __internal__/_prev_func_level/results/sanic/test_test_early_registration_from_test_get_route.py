import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    bp = Blueprint("bp")

    @bp.get("/")
    async def get_method(request):
        return text("I am get method")

    app.blueprint(bp)

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    bp = Blueprint("bp")

    @bp.get("/query")
    async def get_with_query(request):
        param = request.args.get("param", "default")
        return text(f"Query param is {param}")

    app.blueprint(bp)

    request, response = app.test_client.get("/query?param=test")
    assert response.status == 200
    assert response.text == "Query param is test"

    request, response = app.test_client.get("/query")
    assert response.status == 200
    assert response.text == "Query param is default"