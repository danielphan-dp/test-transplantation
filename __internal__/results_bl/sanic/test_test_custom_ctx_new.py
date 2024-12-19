import uuid
import pytest
from sanic import Sanic, response
from sanic.request import Request

def test_get_method():
    app = Sanic("Test")

    @app.get("/get")
    async def get_handler(request: Request):
        return response.text('I am get method')

    _, resp = app.test_client.get("/get")
    
    assert resp.text == 'I am get method'
    assert resp.status == 200

def test_get_method_with_invalid_route():
    app = Sanic("Test")

    @app.get("/get")
    async def get_handler(request: Request):
        return response.text('I am get method')

    _, resp = app.test_client.get("/invalid_route")
    
    assert resp.status == 404

def test_get_method_with_query_params():
    app = Sanic("Test")

    @app.get("/get")
    async def get_handler(request: Request):
        return response.text('I am get method')

    _, resp = app.test_client.get("/get?param=value")
    
    assert resp.text == 'I am get method'
    assert resp.status == 200

def test_get_method_with_headers():
    app = Sanic("Test")

    @app.get("/get")
    async def get_handler(request: Request):
        return response.text('I am get method')

    _, resp = app.test_client.get("/get", headers={"Custom-Header": "value"})
    
    assert resp.text == 'I am get method'
    assert resp.status == 200