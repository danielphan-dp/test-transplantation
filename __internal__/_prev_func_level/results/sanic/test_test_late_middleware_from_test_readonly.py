import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text('I am get method')

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.status_code == 200
    assert response.text == "I am get method"

def test_get_method_with_query_param(app):
    @app.get("/get_with_param")
    def handler(request):
        return text(f"I am get method with param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.status_code == 200
    assert response.text == "I am get method with param: test"

def test_get_method_no_query_param(app):
    @app.get("/get_with_param")
    def handler(request):
        return text(f"I am get method with param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/get_with_param")
    assert response.status_code == 200
    assert response.text == "I am get method with param: none"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status_code == 404
    assert "Requested URL /invalid_route not found" in response.text