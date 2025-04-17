import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_method(app):
    test_client = SanicTestClient(app)
    request, response = test_client.post("/get")
    assert response.status == 405

def test_get_method_not_found(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_empty_response(app):
    @app.get("/empty")
    def empty_method(request):
        return text("")
    
    test_client = SanicTestClient(app)
    request, response = test_client.get("/empty")
    assert response.text == ""
    assert response.status == 200