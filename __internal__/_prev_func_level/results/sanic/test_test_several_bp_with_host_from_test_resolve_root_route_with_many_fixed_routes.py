import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_with_host(app):
    bp = Blueprint("test_bp", url_prefix="/test", host="example.com")

    @bp.route("/get")
    def handler(request):
        return text("I am get method with host")

    app.blueprint(bp)

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.text == "I am get method with host"

def test_get_method_with_invalid_host(app):
    bp = Blueprint("test_bp", url_prefix="/test", host="example.com")

    @bp.route("/get")
    def handler(request):
        return text("I am get method with host")

    app.blueprint(bp)

    headers = {"Host": "invalid.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.status == 404

def test_get_method_with_different_hosts(app):
    bp1 = Blueprint("test_bp1", url_prefix="/test", host="example.com")
    bp2 = Blueprint("test_bp2", url_prefix="/test", host="sub.example.com")

    @bp1.route("/get")
    def handler1(request):
        return text("Hello from example.com")

    @bp2.route("/get")
    def handler2(request):
        return text("Hello from sub.example.com")

    app.blueprint(bp1)
    app.blueprint(bp2)

    headers1 = {"Host": "example.com"}
    request, response = app.test_client.get("/test/get", headers=headers1)
    assert response.text == "Hello from example.com"

    headers2 = {"Host": "sub.example.com"}
    request, response = app.test_client.get("/test/get", headers=headers2)
    assert response.text == "Hello from sub.example.com"