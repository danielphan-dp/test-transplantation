import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/api/v1/test_get")
    def test_get(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/api/v1/test_get")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/api/v1/non_existent_route")
    
    assert response.status == 404
    assert "Requested URL /api/v1/non_existent_route not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/api/v1/test_get?param=value")
    
    assert response.status == 200
    assert response.text == "I am get method"