import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.put("/put_test")
async def put_test(request):
    return text("I am put method")

def test_put_method(app):
    request, response = app.test_client.put("/put_test")
    assert response.status == 200
    assert response.text == "I am put method"

def test_put_method_with_data(app):
    data = "test data"
    request, response = app.test_client.put("/put_test", data=data)
    assert response.status == 200
    assert response.text == "I am put method"

def test_put_method_with_empty_data(app):
    request, response = app.test_client.put("/put_test", data="")
    assert response.status == 200
    assert response.text == "I am put method"

def test_put_method_with_invalid_route(app):
    request, response = app.test_client.put("/invalid_route")
    assert response.status == 404

def test_put_method_with_headers(app):
    headers = {"Content-Type": "application/json"}
    request, response = app.test_client.put("/put_test", headers=headers)
    assert response.status == 200
    assert response.text == "I am put method"