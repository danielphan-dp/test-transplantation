import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import TestManager

@pytest.fixture
def app():
    app = Sanic("test_app")

    class DummyView:
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView().get, "/")
    return app

def test_get_method_response(app):
    manager = TestManager(app)
    request, response = manager.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    manager = TestManager(app)
    request, response = manager.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param(app):
    manager = TestManager(app)
    request, response = manager.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming no change in response for query params

def test_get_method_with_invalid_method(app):
    manager = TestManager(app)
    request, response = manager.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text