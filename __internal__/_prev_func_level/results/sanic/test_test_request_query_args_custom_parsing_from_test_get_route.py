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
    assert response.status == 200
    assert request.get_query_args(keep_blank_values=True) == [
        ("param1", "value1"),
        ("param2", "value2"),
    ]
    assert request.query_args == [("param1", "value1"), ("param2", "value2")]

def test_get_method_with_empty_query_param(app):
    request, response = app.test_client.get("/?param1=value1&param2=")
    assert response.status == 200
    assert request.get_query_args(keep_blank_values=True) == [
        ("param1", "value1"),
        ("param2", ""),
    ]
    assert request.query_args == [("param1", "value1")]

def test_get_method_with_no_query_params(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert request.get_query_args(keep_blank_values=True) == []
    assert request.query_args == []

def test_get_method_with_multiple_empty_query_params(app):
    request, response = app.test_client.get("/?param1=&param2=&param3=")
    assert response.status == 200
    assert request.get_query_args(keep_blank_values=True) == [
        ("param1", ""),
        ("param2", ""),
        ("param3", ""),
    ]
    assert request.query_args == []