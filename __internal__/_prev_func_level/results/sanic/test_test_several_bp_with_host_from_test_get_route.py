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
            return text("I am get method")

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_host(app):
    bp = Blueprint("test_bp", url_prefix="/test", host="example.com")

    @bp.route("/")
    def handler(request):
        return text("Hello from host")

    app.blueprint(bp)

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/test/", headers=headers)
    assert response.status == 200
    assert response.text == "Hello from host"

def test_get_method_with_invalid_host(app):
    bp = Blueprint("test_bp_invalid", url_prefix="/test", host="example.com")

    @bp.route("/")
    def handler(request):
        return text("Hello from invalid host")

    app.blueprint(bp)

    headers = {"Host": "invalid.com"}
    request, response = app.test_client.get("/test/", headers=headers)
    assert response.status == 404

def test_get_method_with_different_hosts(app):
    bp1 = Blueprint("test_bp1", url_prefix="/test1", host="example.com")
    bp2 = Blueprint("test_bp2", url_prefix="/test2", host="sub.example.com")

    @bp1.route("/")
    def handler1(request):
        return text("Hello from example.com")

    @bp2.route("/")
    def handler2(request):
        return text("Hello from sub.example.com")

    app.blueprint(bp1)
    app.blueprint(bp2)

    headers1 = {"Host": "example.com"}
    request, response = app.test_client.get("/test1/", headers=headers1)
    assert response.status == 200
    assert response.text == "Hello from example.com"

    headers2 = {"Host": "sub.example.com"}
    request, response = app.test_client.get("/test2/", headers=headers2)
    assert response.status == 200
    assert response.text == "Hello from sub.example.com"