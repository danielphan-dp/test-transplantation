import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.get("/get")
def get_response(request):
    return text('I am get method')

def test_get_method_response(app):
    _, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_status_code(app):
    _, response = app.test_client.get("/get")
    assert response.status == 200

def test_get_method_invalid_route(app):
    _, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    def get_with_params(request):
        return text(f"Received param: {request.args.get('param', 'none')}")

    _, response = app.test_client.get("/get_with_params?param=test")
    assert response.text == "Received param: test"