import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def client(app):
    return app.test_client

class DummyView:
    def get(self, request):
        return text('I am get method')

def test_get_method_response(app, client):
    app.add_route(DummyView.get, "/")
    request, response = client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app, client):
    request, response = client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_param(app, client):
    @app.route("/<param>")
    def handler(request, param):
        return text(f"Received param: {param}")

    request, response = client.get("/test_param")
    assert response.status == 200
    assert response.text == "Received param: test_param"

def test_get_method_with_headers(app, client):
    @app.route("/")
    def handler(request):
        return text("Headers received", headers={"X-Custom-Header": "Value"})

    request, response = client.get("/")
    assert response.status == 200
    assert response.headers["X-Custom-Header"] == "Value"