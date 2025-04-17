import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method():
    app = Sanic(name="Test")

    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")

    assert response.text == 'I am get method'
    assert response.status == 200
    assert request.endpoint == "Test.get_method"

def test_get_method_not_found():
    app = Sanic(name="Test")

    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/nonexistent")

    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param():
    app = Sanic(name="Test")

    @app.route("/get")
    def get_method(request):
        param = request.args.get('param', 'default')
        return text(f'I am get method with param: {param}')

    request, response = app.test_client.get("/get?param=test")

    assert response.text == 'I am get method with param: test'
    assert response.status == 200

def test_get_method_with_empty_query_param():
    app = Sanic(name="Test")

    @app.route("/get")
    def get_method(request):
        param = request.args.get('param', 'default')
        return text(f'I am get method with param: {param}')

    request, response = app.test_client.get("/get?param=")

    assert response.text == 'I am get method with param: '
    assert response.status == 200