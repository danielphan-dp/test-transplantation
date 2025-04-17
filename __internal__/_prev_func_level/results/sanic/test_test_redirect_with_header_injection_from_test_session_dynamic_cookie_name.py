import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("test_app")

@app.route("/get")
def get(request):
    return text("I am get method")

@pytest.fixture
def test_client():
    return app.test_client

def test_get_method_response(test_client):
    request, response = test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(test_client):
    request, response = test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_headers(test_client):
    request, response = test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert "Custom-Header" in response.headers

def test_get_method_empty_response(test_client):
    @app.route("/empty")
    def empty_response(request):
        return text("")
    
    request, response = test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""