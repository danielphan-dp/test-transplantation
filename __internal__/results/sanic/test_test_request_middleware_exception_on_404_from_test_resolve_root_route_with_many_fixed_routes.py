import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.route("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    @app.route("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/not-found")
    
    assert response.status == 404
    assert "Requested URL /not-found not found" in response.text

def test_get_method_with_middleware(app):
    results = []

    @app.middleware
    async def middleware(request):
        results.append(request)

    @app.route("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    
    assert response.text == "I am get method"
    assert len(results) == 1
    assert results[0] is not None

def test_get_method_with_custom_header(app):
    @app.route("/")
    async def handler(request):
        return text("I am get method", headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.headers["X-Custom-Header"] == "value"