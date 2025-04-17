import pytest
from unittest.mock import Mock
from sanic import Sanic
from sanic.response import text
from sanic_testing import TestManager

app = Sanic("test_app")

@app.route("/")
def get(request):
    return text("I am get method")

@pytest.fixture
def test_client():
    manager = TestManager(app)
    return manager.test_client

def test_get_method_response(test_client):
    request, response = test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(test_client):
    request, response = test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_headers(test_client):
    request, response = test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"