import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_invalid_post(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    def handler(request):
        return text(f"Received param: {request.args.get('param')}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.text == "Received param: test"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404

def test_get_method_with_headers(app):
    @app.get("/get_with_headers")
    def handler(request):
        return text(request.headers.get('Custom-Header', 'No Header'))

    request, response = app.test_client.get("/get_with_headers", headers={'Custom-Header': 'HeaderValue'})
    assert response.text == "HeaderValue"