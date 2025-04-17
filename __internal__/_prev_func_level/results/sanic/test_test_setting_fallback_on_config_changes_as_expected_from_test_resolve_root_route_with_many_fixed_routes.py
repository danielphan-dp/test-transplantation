import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_returns_plain_text(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.text == "I am get method"

def test_get_method_with_different_route(app):
    @app.get("/another_test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/another_test")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/test_with_params")
    def get_method(request):
        return text(f"I am get method with param: {request.args.get('param')}")

    request, response = app.test_client.get("/test_with_params?param=test")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.text == "I am get method with param: test"