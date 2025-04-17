import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    return app

def test_get_route(app):
    request, response = app.test_client.get("/get")
    assert response.status_code == 200
    assert response.text == "I am get method"

def test_get_route_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status_code == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_route_with_query_param(app):
    @app.get("/get_with_param")
    def get_with_param_handler(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.status_code == 200
    assert response.text == "Received param: test"