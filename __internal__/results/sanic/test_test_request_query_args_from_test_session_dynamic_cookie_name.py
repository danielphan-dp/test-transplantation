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

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert request.query_args == [("param", "value")]
    assert response.text == "I am get method"

def test_get_method_no_params(app):
    request, response = app.test_client.get("/get")
    assert not request.query_args
    assert response.text == "I am get method"

def test_get_method_multiple_params(app):
    params = [("param1", "value1"), ("param2", "value2")]
    request, response = app.test_client.get("/get", params=params)
    assert request.query_args == params
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_special_characters(app):
    request, response = app.test_client.get("/get?param=sp@cial#chars")
    assert request.query_args == [("param", "sp@cial#chars")]
    assert response.text == "I am get method"