import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_logging(app, caplog):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text("I am get method")

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert "I am get method" in caplog.text

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("response")
    async def process_response(request, response):
        results.append(response)

    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")

    assert response.text == "I am get method"
    assert len(results) == 1
    assert isinstance(results[0], type(response))