import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/get", methods=["GET"])
    async def handler(request):
        return text("I am get method")
    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_empty_query_params(app):
    request, response = app.test_client.get("/get?param=")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404