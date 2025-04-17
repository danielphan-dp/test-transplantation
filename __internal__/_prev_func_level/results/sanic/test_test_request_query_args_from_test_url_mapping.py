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
    assert response.text == "I am get method"

def test_get_method_no_query_params(app):
    request, response = app.test_client.get("/")
    assert not request.query_args
    assert response.text == "I am get method"

def test_get_method_with_empty_query_params(app):
    request, response = app.test_client.get("/?param=")
    assert request.query_args == [("param", "")]
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_special_characters(app):
    request, response = app.test_client.get("/?param=hello%20world")
    assert request.query_args == [("param", "hello world")]
    assert response.text == "I am get method"