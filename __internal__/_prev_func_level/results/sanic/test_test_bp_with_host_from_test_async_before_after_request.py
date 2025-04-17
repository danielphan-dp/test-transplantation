import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_with_host(app):
    bp = Blueprint("test_bp", url_prefix="/test", host="example.com")

    @bp.route("/get")
    def get_method(request):
        return text("I am get method")

    app.blueprint(bp)

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.text == "I am get method"

    headers = {"Host": "sub.example.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.status == 404

def test_get_method_invalid_host(app):
    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    headers = {"Host": "invalid.example.com"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == "I am get method"  # Should still return valid response regardless of host

def test_get_method_no_host(app):
    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"  # Ensure it works without host header

def test_get_method_with_different_hosts(app):
    bp = Blueprint("test_bp", url_prefix="/test")

    @bp.route("/get", host="example.com")
    def get_method_example(request):
        return text("I am get method for example.com")

    @bp.route("/get", host="sub.example.com")
    def get_method_sub(request):
        return text("I am get method for sub.example.com")

    app.blueprint(bp)

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.text == "I am get method for example.com"

    headers = {"Host": "sub.example.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.text == "I am get method for sub.example.com"