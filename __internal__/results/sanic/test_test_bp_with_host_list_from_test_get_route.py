import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_host(app):
    bp = Blueprint("test_bp_host", url_prefix="/test", host=["example.com"])

    @bp.route("/")
    def handler(request):
        return text("I am get method with host")

    app.blueprint(bp)

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/test/", headers=headers)
    assert response.status == 200
    assert response.text == "I am get method with host"

    headers = {"Host": "sub.example.com"}
    request, response = app.test_client.get("/test/", headers=headers)
    assert response.status == 404

def test_get_method_invalid_host(app):
    @app.get("/")
    def get_method(request):
        return text("I am get method")

    headers = {"Host": "invalid.example.com"}
    request, response = app.test_client.get("/", headers=headers)
    assert response.status == 404

def test_get_method_with_different_hosts(app):
    bp = Blueprint("test_bp_host", url_prefix="/test", host=["example.com", "sub.example.com"])

    @bp.route("/")
    def handler1(request):
        return text("Hello from main host")

    @bp.route("/", host=["sub.example.com"])
    def handler2(request):
        return text("Hello from subdomain")

    app.blueprint(bp)

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/test/", headers=headers)
    assert response.text == "Hello from main host"

    headers = {"Host": "sub.example.com"}
    request, response = app.test_client.get("/test/", headers=headers)
    assert response.text == "Hello from subdomain"

    headers = {"Host": "nonexistent.example.com"}
    request, response = app.test_client.get("/test/", headers=headers)
    assert response.status == 404