import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import TestManager

app = Sanic("test_app")

@app.get("/")
async def get_method(request):
    return text('I am get method')

@pytest.fixture
def test_client():
    manager = TestManager(app)
    return manager.test_client

def test_get_method_response(test_client):
    request, response = test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(test_client):
    request, response = test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_headers(test_client):
    request, response = test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'