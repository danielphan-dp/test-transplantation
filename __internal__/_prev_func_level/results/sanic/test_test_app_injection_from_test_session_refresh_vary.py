import random
from sanic import Sanic
from sanic.response import text
import json
from ujson import loads

app = Sanic("test")

@app.get("/get")
def get_method(request):
    return text('I am get method')

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == 'I am get method'
    assert response.status == 200
    assert response.headers.get("Custom-Header") is None

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_random_data(app):
    expected = random.choice(range(0, 100))
    @app.listener("after_server_start")
    async def inject_data(app, loop):
        app.ctx.injected = expected

    @app.get("/")
    async def handler(request):
        return json({"injected": request.app.ctx.injected})

    request, response = app.test_client.get("/")
    response_json = loads(response.text)
    assert response_json["injected"] == expected