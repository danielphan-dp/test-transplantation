import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_with_query")
    def get_with_query(request):
        name = request.args.get("name", "Guest")
        return text(f"Hello, {name}")

    request, response = app.test_client.get("/get_with_query?name=John")
    
    assert response.text == "Hello, John"

    request, response = app.test_client.get("/get_with_query")
    
    assert response.text == "Hello, Guest"