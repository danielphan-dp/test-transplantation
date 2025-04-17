import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("response")
    async def process_response(request, response):
        results.append(response)

    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == 'I am get method'
    assert len(results) == 1
    assert isinstance(results[0], type(response))  # Ensure the response is captured in middleware

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")

    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_invalid_route(app):
    request, response = app.test_client.post("/get")

    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text