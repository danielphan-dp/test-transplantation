import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import NotFound

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/")
    async def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("response")
    async def process_response(request, response):
        results.append(response)
        return response

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert len(results) == 1
    assert isinstance(results[0], type(response))  # Check if the response is of the same type

def test_get_method_with_custom_error_handler(app):
    @app.exception(NotFound)
    async def error_handler(request, exception):
        return text("Custom Not Found", status=404)

    request, response = app.test_client.get("/invalid_route")
    assert response.text == "Custom Not Found"
    assert response.status == 404