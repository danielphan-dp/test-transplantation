import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    blueprint = Blueprint("test_get_method_response")

    @blueprint.route("/get", methods=["GET"])
    def get_method(request):
        return text("I am get method")

    app.blueprint(blueprint)
    
    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("request")
    async def request_middleware(request):
        results.append("Request middleware executed")

    @app.middleware("response")
    async def response_middleware(request, response):
        results.append("Response middleware executed")

    blueprint = Blueprint("test_get_method_with_middleware")

    @blueprint.route("/get", methods=["GET"])
    def get_method(request):
        return text("I am get method")

    app.blueprint(blueprint)

    request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == "I am get method"
    assert results == ["Request middleware executed", "Response middleware executed"]

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_invalid_method(app):
    blueprint = Blueprint("test_get_method_invalid_method")

    @blueprint.route("/get", methods=["GET"])
    def get_method(request):
        return text("I am get method")

    app.blueprint(blueprint)

    request, response = app.test_client.post("/get")
    
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text