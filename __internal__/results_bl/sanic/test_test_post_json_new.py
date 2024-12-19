import json
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/", methods=["GET"])
async def get_handler(request):
    return text("I am get method")

def test_get_method(app):
    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.body == b"I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=test")
    
    assert response.status == 200
    assert response.body == b"I am get method"