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
    bp = Blueprint("test_bp_host", url_prefix="/test", host=["example.com"])

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

    headers = {"Host": "nonexistent.example.com"}
    request, response = app.test_client.get("/test/get", headers=headers)
    assert response.status == 404

    route_names = [r.name for r in app.router.routes]
    assert "test_get_method_with_host.test_bp_host.get_method" in route_names

def test_get_method_invalid_host(app):
    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    headers = {"Host": "invalid.example.com"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == "I am get method"  # Should still return the method response

def test_get_method_no_host(app):
    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"  # Test without host header