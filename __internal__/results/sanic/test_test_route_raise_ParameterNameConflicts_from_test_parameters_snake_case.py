import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/test-get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/test-get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_parameters(app):
    @app.get("/test-get/<param>")
    def handler(request, param):
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/test-get/test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_with_empty_response(app):
    @app.get("/test-get-empty")
    def handler(request):
        return text("")

    request, response = app.test_client.get("/test-get-empty")
    assert response.status == 200
    assert response.text == ""

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_with_conflicting_parameters(app):
    @app.get("/api/v1/<user>/<user>/")
    def handler(request, user):
        return text("OK")

    with pytest.raises(ParameterNameConflicts):
        app.router.finalize()