import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    bp = Blueprint("test_bp", url_prefix="/test", host="example.com")

    @bp.route("/")
    def get_handler(request):
        return text("I am get method")

    app.blueprint(bp)

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/test/", headers=headers)
    assert response.text == "I am get method"

def test_get_method_with_invalid_host(app):
    bp = Blueprint("test_bp", url_prefix="/test", host="example.com")

    @bp.route("/")
    def get_handler(request):
        return text("I am get method")

    app.blueprint(bp)

    headers = {"Host": "invalid.com"}
    request, response = app.test_client.get("/test/", headers=headers)
    assert response.status == 404

def test_get_method_with_subdomain(app):
    bp = Blueprint("test_bp", url_prefix="/test", host="example.com")

    @bp.route("/", host="sub.example.com")
    def subdomain_handler(request):
        return text("I am get method from subdomain")

    app.blueprint(bp)

    headers = {"Host": "sub.example.com"}
    request, response = app.test_client.get("/test/", headers=headers)
    assert response.text == "I am get method from subdomain"

def test_get_method_with_different_http_method(app):
    bp = Blueprint("test_bp", url_prefix="/test", host="example.com")

    @bp.route("/", methods=["GET"])
    def get_handler(request):
        return text("I am get method")

    app.blueprint(bp)

    headers = {"Host": "example.com"}
    request, response = app.test_client.post("/test/", headers=headers)
    assert response.status == 405
    assert "Method POST not allowed for URL /test/" in response.text