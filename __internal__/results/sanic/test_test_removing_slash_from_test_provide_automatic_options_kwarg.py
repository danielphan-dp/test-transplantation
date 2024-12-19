import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.post("/test")
    async def post(request):
        return text('I am post method')

    request, response = app.test_client.post("/test")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_not_found(app):
    request, response = app.test_client.post("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_post_method_with_data(app):
    @app.post("/data")
    async def post(request):
        return text(f"Received: {request.json}")

    request, response = app.test_client.post("/data", json={"key": "value"})
    assert response.status == 200
    assert response.text == 'Received: {"key": "value"}'

def test_post_method_with_empty_data(app):
    @app.post("/empty")
    async def post(request):
        return text("Received empty data")

    request, response = app.test_client.post("/empty", json={})
    assert response.status == 200
    assert response.text == "Received empty data"