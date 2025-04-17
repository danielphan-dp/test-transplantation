import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get-test")
    async def handler(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get-test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_path(app):
    request, response = app.test_client.get("/invalid-path")
    assert response.status == 404
    assert "Requested URL /invalid-path not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get-test?param=value")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/get-test", headers=headers)
    assert response.status == 200
    assert response.text == "I am get method"