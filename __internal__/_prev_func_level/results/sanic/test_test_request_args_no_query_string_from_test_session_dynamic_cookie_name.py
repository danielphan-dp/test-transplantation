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

def test_get_method_no_query_string(app):
    request, response = app.test_client.get("/get")
    assert request.args == {}

def test_get_method_with_query_string(app):
    request, response = app.test_client.get("/get?param=value")
    assert request.args == {"param": "value"}
    assert response.text == "I am get method"