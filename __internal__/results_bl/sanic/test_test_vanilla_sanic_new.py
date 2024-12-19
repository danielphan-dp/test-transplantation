import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic(__name__)
    return app

@app.get("/")
async def get_method(request):
    return text('I am get method')

def test_get_method(app):
    _, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param(app):
    _, response = app.test_client.get("/?param=value")
    assert response.text == "I am get method"

def test_get_method_empty_request(app):
    _, response = app.test_client.get("/")
    assert response.text == "I am get method"