import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_patch(app):
    @app.patch("/get")
    def handler(request):
        return text("This should not be reachable")

    request, response = app.test_client.patch("/get")
    assert response.status == 405

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    def handler(request):
        return text(f"Received param: {request.args.get('param')}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.text == "Received param: test"
    assert response.status == 200

def test_get_method_no_content(app):
    @app.get("/get_no_content")
    def handler(request):
        return text("")

    request, response = app.test_client.get("/get_no_content")
    assert response.text == ""
    assert response.status == 200