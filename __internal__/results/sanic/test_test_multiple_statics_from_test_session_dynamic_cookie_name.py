import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get", methods=["GET"])
    def get(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent")
    assert response.status == 404
    assert "Requested URL /non_existent not found" in response.text

def test_get_method_with_query_params(app):
    @app.route("/get_with_params", methods=["GET"])
    def get_with_params(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

    request, response = app.test_client.get("/get_with_params")
    assert response.status == 200
    assert response.text == "Received param: default"