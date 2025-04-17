import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param(app):
    @app.get("/greet")
    def greet(request):
        name = request.args.get("name", "World")
        return text(f"Hello, {name}!")

    request, response = app.test_client.get("/greet?name=Alice")
    assert response.status == 200
    assert response.text == "Hello, Alice!"

def test_get_method_with_empty_query_param(app):
    @app.get("/greet")
    def greet(request):
        name = request.args.get("name", "World")
        return text(f"Hello, {name}!")

    request, response = app.test_client.get("/greet?name=")
    assert response.status == 200
    assert response.text == "Hello, !"  # Edge case with empty query param

def test_get_method_with_non_string_response(app):
    @app.get("/number")
    def return_number(request):
        return text(123)  # This should raise a TypeError

    with pytest.raises(TypeError):
        app.test_client.get("/number")