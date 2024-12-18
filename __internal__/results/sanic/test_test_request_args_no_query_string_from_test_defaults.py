import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_request_args(app):
    request, response = app.test_client.get("/")
    assert request.args == {}

def test_get_method_content_type(app):
    request, response = app.test_client.get("/")
    assert response.content_type == "text/plain; charset=utf-8"

def test_get_method_empty_query_string(app):
    request, response = app.test_client.get("/?foo=bar")
    assert request.args == {'foo': ['bar']}

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/", headers={"X-Custom-Header": "value"})
    assert request.headers.get("X-Custom-Header") == "value"