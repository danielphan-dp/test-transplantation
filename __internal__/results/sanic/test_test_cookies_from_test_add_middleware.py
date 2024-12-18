import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/test")
    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/test?param=value")
    assert response.text == "I am get method"

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/test", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"

def test_get_method_with_empty_request(app):
    request, response = app.test_client.get("/test", data={})
    assert response.text == "I am get method"