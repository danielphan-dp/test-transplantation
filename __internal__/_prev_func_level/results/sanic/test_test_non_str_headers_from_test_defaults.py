import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    async def handler(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_headers(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "Value"})
    assert response.headers.get("Content-Type") == "text/plain; charset=utf-8"

def test_get_method_with_non_str_headers(app):
    request, response = app.test_client.get("/get", headers={"answer": 42})
    assert response.headers.get("answer") is None

def test_get_method_empty_response(app):
    @app.route("/empty")
    async def empty_handler(request):
        return text('')

    request, response = app.test_client.get("/empty")
    assert response.text == ''
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text