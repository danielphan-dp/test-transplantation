import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method_default(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_host_header(app):
    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_different_methods(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405

def test_get_method_with_empty_host(app):
    headers = {"Host": ""}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == 'I am get method'