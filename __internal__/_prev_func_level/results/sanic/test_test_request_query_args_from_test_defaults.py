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

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param1=value1&param2=value2")
    assert request.query_args == [("param1", "value1"), ("param2", "value2")]

def test_get_method_no_query_params(app):
    request, response = app.test_client.get("/")
    assert not request.query_args

def test_get_method_with_single_query_param(app):
    request, response = app.test_client.get("/?param=value")
    assert request.query_args == [("param", "value")]

def test_get_method_with_duplicate_query_params(app):
    request, response = app.test_client.get("/?param=value1&param=value2")
    assert request.query_args == [("param", "value1"), ("param", "value2")]

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/", headers={"X-Custom-Header": "value"})
    assert request.headers.get("X-Custom-Header") == "value"