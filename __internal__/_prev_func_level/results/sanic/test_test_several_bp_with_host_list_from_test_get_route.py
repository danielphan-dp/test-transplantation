import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    class DummyView:
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_host(app):
    bp = Blueprint("test_bp", url_prefix="/test", host=["example.com"])

    @bp.route("/get")
    def handler(request):
        return text("I am get method")

    app.blueprint(bp)

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.status == 200
    assert response.text == "I am get method"

    headers = {"Host": "invalid.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.status == 404

def test_get_method_with_different_hosts(app):
    bp = Blueprint("test_bp", url_prefix="/test", host=["example.com", "sub.example.com"])

    @bp.route("/get")
    def handler(request):
        return text("I am get method")

    app.blueprint(bp)

    headers = {"Host": "sub.example.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.status == 200
    assert response.text == "I am get method"

    headers = {"Host": "another.example.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.status == 404

def test_get_method_with_invalid_route(app):
    class DummyView:
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView().get, "/valid")

    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text