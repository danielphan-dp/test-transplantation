import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def handler(request):
    return text("I am get method")

def test_get_method_response(app):
    bp = Blueprint("Test", version=1.1, version_prefix="/test/v")
    bp.route("/get")(handler)
    app.blueprint(bp, version=1.2, version_prefix="/api/v")

    request, response = app.test_client.get("/api/v1.2/test/v/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/api/v1.2/test/v/invalid")
    assert response.status == 404
    assert "Requested URL /api/v1.2/test/v/invalid not found" in response.text

def test_get_method_with_query_param(app):
    bp = Blueprint("Test", version=1.1, version_prefix="/test/v")
    @bp.route("/get")
    def get_with_param(request):
        param = request.args.get('param', 'default')
        return text(f"I am get method with param: {param}")

    app.blueprint(bp, version=1.2, version_prefix="/api/v")

    request, response = app.test_client.get("/api/v1.2/test/v/get?param=test")
    assert response.status == 200
    assert response.text == "I am get method with param: test"