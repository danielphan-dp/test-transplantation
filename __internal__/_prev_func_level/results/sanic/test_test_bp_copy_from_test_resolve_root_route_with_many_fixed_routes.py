import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    bp = Blueprint("test_bp", version=1)

    @bp.get("/get")
    def get_method(request):
        return text("I am get method")

    app.blueprint(bp)

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    bp = Blueprint("test_bp_invalid", version=1)

    @bp.get("/get")
    def get_method(request):
        return text("I am get method")

    app.blueprint(bp)

    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_context(app):
    bp = Blueprint("test_bp_context", version=1)
    bp.ctx.test = "context_value"

    @bp.get("/get_context")
    def get_method(request):
        return text(f"Context value is {request.ctx.test}")

    app.blueprint(bp)

    request, response = app.test_client.get("/get_context")
    assert response.status == 200
    assert response.text == "Context value is context_value"