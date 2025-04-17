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
    assert response.headers["Custom-Header"] == "value"  # This will not be present, just to check header handling

def test_get_method_with_query_params(test_client):
    request, response = test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Ensure query params do not affect response

def test_get_method_empty_request(test_client):
    request, response = test_client.get("/get", data={})
    assert response.status == 200
    assert response.text == "I am get method"  # Ensure empty data does not affect response