import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/")
    async def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("response")
    async def process_response(request, response):
        results.append(response)
        return response

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"
    assert len(results) == 1
    assert isinstance(results[0], type(response))