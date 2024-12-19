import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import NotFound

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404
    assert response.text == "OK"

def test_get_method_with_middleware(app):
    result = {"status_code": "middleware not run"}

    @app.middleware("response")
    async def process_response(request, response):
        result["status_code"] = response.status
        return response

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert result["status_code"] == 200

def test_get_method_with_exception(app):
    @app.exception(NotFound)
    async def error_handler(request, exception):
        return text("Handled Not Found", exception.status_code)

    request, response = app.test_client.get("/page_not_found")
    assert response.text == "Handled Not Found"
    assert response.status == 404