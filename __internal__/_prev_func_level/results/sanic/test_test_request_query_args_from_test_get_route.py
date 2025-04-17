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
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param1=value1&param2=value2")
    assert request.query_args == [("param1", "value1"), ("param2", "value2")]

def test_get_method_no_query_params(app):
    request, response = app.test_client.get("/")
    assert not request.query_args

def test_get_method_with_single_param(app):
    request, response = app.test_client.get("/?param=value")
    assert request.query_args == [("param", "value")]

def test_get_method_with_empty_response(app):
    @app.get("/empty")
    def empty_handler(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""