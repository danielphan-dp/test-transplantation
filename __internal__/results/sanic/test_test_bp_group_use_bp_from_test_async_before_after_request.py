import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def handler(request):
    return text("I am get method")

def test_get_method_response(app):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group)

    request, response = app.test_client.get("/v1.1")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_param(app):
    @app.route("/v1.1")
    def get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/v1.1?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"