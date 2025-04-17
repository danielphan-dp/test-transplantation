import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_param(app):
    @app.get("/greet")
    async def greet(request):
        name = request.args.get('name', 'World')
        return text(f"Hello, {name}!")

    request, response = app.test_client.get("/greet?name=Alice")
    assert response.status == 200
    assert response.text == "Hello, Alice!"

def test_get_method_with_empty_query_param(app):
    @app.get("/greet")
    async def greet(request):
        name = request.args.get('name', 'World')
        return text(f"Hello, {name}!")

    request, response = app.test_client.get("/greet?name=")
    assert response.status == 200
    assert response.text == "Hello, !"  # Edge case with empty name

def test_get_method_with_non_string_query_param(app):
    @app.get("/greet")
    async def greet(request):
        name = request.args.get('name', 'World')
        return text(f"Hello, {name}!")

    request, response = app.test_client.get("/greet?name=123")
    assert response.status == 200
    assert response.text == "Hello, 123!"  # Non-string query param

def test_get_method_with_middleware(app):
    results = []

    @app.middleware
    async def handler(request):
        results.append(request)

    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert len(results) == 1
    assert results[0] is request