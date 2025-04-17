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
    bp = Blueprint("test_bp", url_prefix="/test", host=["example.com"])

    @bp.route("/get")
    def get_method(request):
        return text("I am get method")

    app.blueprint(bp)

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.text == "I am get method"

    headers = {"Host": "invalid.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.status == 404

def test_get_method_with_different_hosts(app):
    bp = Blueprint("test_bp", url_prefix="/test", host=["example.com", "sub.example.com"])

    @bp.route("/get")
    def get_method(request):
        return text("I am get method")

    app.blueprint(bp)

    headers = {"Host": "sub.example.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.text == "I am get method"

    headers = {"Host": "another.example.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.status == 404

def test_get_method_with_invalid_path(app):
    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/invalid_path")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get")
    def get_method(request):
        return text("I am get method with query params")

    request, response = app.test_client.get("/get?param=value")
    assert response.text == "I am get method with query params"