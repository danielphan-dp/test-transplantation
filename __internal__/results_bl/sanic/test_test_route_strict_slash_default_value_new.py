import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("test_get_method")

@app.get("/get")
def handler(request):
    return text("I am get method")

def test_get_method_success():
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found():
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_strict_slash():
    app = Sanic("test_route_strict_slash", strict_slashes=True)

    @app.get("/get")
    def handler(request):
        return text("OK")

    request, response = app.test_client.get("/get/")
    assert response.status == 404

def test_get_method_with_query_params():
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"