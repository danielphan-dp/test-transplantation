import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.get("/get")
    def get_handler(request):
        return text("OK")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "OK"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "OK"

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get", headers={"Content-Length": "0"})
    assert response.status == 200
    assert response.text == "OK"