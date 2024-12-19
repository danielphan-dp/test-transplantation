import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get_method", methods=["GET"])
    async def get_method(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get_method")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404

def test_get_method_invalid_method(app):
    request, response = app.test_client.post("/get_method")
    assert response.status == 405

def test_get_method_with_query_params(app):
    @app.route("/get_method_with_params", methods=["GET"])
    async def get_method_with_params(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_method_with_params?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

    request, response = app.test_client.get("/get_method_with_params")
    assert response.status == 200
    assert response.text == "Received param: default"