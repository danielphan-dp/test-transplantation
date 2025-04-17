import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_with_host(app):
    bp = Blueprint("test_bp", url_prefix="/test", host="example.com")

    @bp.route("/")
    def get_method(request):
        return text("I am get method")

    app.blueprint(bp)

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/test/", headers=headers)
    assert response.text == "I am get method"

    headers = {"Host": "sub.example.com"}
    request, response = app.test_client.get("/test/", headers=headers)
    assert response.status == 404

def test_get_method_with_invalid_host(app):
    bp = Blueprint("test_bp_invalid", url_prefix="/test_invalid", host="example.com")

    @bp.route("/")
    def get_method_invalid(request):
        return text("This should not be reachable")

    app.blueprint(bp)

    headers = {"Host": "invalid.example.com"}
    request, response = app.test_client.get("/test_invalid/", headers=headers)
    assert response.status == 404

def test_get_method_with_no_host(app):
    bp = Blueprint("test_bp_no_host", url_prefix="/test_no_host")

    @bp.route("/")
    def get_method_no_host(request):
        return text("I am get method without host")

    app.blueprint(bp)

    request, response = app.test_client.get("/test_no_host/")
    assert response.text == "I am get method without host"