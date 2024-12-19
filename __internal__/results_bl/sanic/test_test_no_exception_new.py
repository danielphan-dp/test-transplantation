import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/")
    async def test_get(request):
        return text("I am get method")
    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_invalid_method(app):
    request, response = app.test_client.post("/")
    assert response.status == 405

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/", headers={"Content-Length": "0"})
    assert response.status == 200
    assert response.text == "I am get method"