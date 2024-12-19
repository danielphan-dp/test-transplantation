import pytest
from sanic import Sanic, Blueprint, text

def test_get_method():
    app = Sanic("TestApp")
    
    @app.route("/")
    async def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_not_found():
    app = Sanic("TestApp")
    
    @app.route("/")
    async def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params():
    app = Sanic("TestApp")
    
    @app.route("/")
    async def get_method(request):
        return text(f'I am get method with params: {request.args}')

    _, response = app.test_client.get("/?param1=value1&param2=value2")
    assert response.text == "I am get method with params: {'param1': ['value1'], 'param2': ['value2']}"