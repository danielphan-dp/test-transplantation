import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    class DummyView:
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView().get, "/")
    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent")
    assert response.status == 404
    assert "Requested URL /non_existent not found" in response.text

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("response")
    async def process_response(request, response):
        results.append(response)
        return response

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert len(results) == 1
    assert isinstance(results[0], type(response))  # Ensure it's the same response type

def test_get_method_with_custom_status(app):
    class CustomView:
        def get(self, request):
            return text("Custom Status", status=201)

    app.add_route(CustomView().get, "/custom_status")
    request, response = app.test_client.get("/custom_status")
    assert response.status == 201
    assert response.text == "Custom Status"