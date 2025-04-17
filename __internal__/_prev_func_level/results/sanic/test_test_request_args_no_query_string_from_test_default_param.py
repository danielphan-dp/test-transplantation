import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/test-get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/test-get")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_no_query_string(app):
    @app.get("/test-get-no-query")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/test-get-no-query")

    assert request.args == {}
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_query_string(app):
    @app.get("/test-get-with-query")
    def handler(request):
        return text("I am get method with query")

    request, response = app.test_client.get("/test-get-with-query?param=value")

    assert request.args == {'param': ['value']}
    assert response.status == 200
    assert response.text == "I am get method with query"