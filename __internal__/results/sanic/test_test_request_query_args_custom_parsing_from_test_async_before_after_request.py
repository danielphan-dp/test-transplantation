import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_args(app):
    request, response = app.test_client.get("/get?param1=value1&param2=value2")
    assert response.text == "I am get method"
    assert request.get_query_args() == [("param1", "value1"), ("param2", "value2")]

def test_get_method_empty_query_args(app):
    request, response = app.test_client.get("/get?")
    assert response.text == "I am get method"
    assert request.get_query_args() == []

def test_get_method_with_blank_query_arg(app):
    request, response = app.test_client.get("/get?param1=&param2=value2")
    assert response.text == "I am get method"
    assert request.get_query_args(keep_blank_values=True) == [("param1", ""), ("param2", "value2")]

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert request.headers.get("Custom-Header") == "value"