import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("test_app")

@app.route("/")
def get_method(request):
    return text("I am get method")

@pytest.fixture
def test_client():
    return app.test_client

def test_get_method_returns_correct_content(test_client):
    request, response = test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_status_code(test_client):
    request, response = test_client.get("/")
    assert response.status == 200

def test_get_method_content_type(test_client):
    request, response = test_client.get("/")
    assert response.content_type == "text/plain; charset=utf-8"

def test_get_method_empty_query_params(test_client):
    request, response = test_client.get("/?param=")
    assert response.text == "I am get method"  # Ensure it still returns the correct content

def test_get_method_with_headers(test_client):
    request, response = test_client.get("/", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.headers.get("Custom-Header") is None  # Custom headers should not affect response