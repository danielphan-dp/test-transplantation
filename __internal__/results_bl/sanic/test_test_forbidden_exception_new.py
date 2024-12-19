import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import Forbidden

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/test")
    async def test_get(request):
        return text("I am get method")
    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_forbidden(app):
    request, response = app.test_client.get("/403")
    assert response.status == 403

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_invalid_request(app):
    request, response = app.test_client.get("/test", headers={"Invalid-Header": "value"})
    assert response.status == 400  # Assuming the app handles invalid headers with a BadRequest response