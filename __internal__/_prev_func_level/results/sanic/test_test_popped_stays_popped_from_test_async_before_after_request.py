import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    async def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_params(app):
    request, response = app.test_client.get("/get", params=[("param1", "value1")])
    assert response.text == "I am get method"
    assert request.args.get("param1") == ["value1"]

def test_get_method_no_params(app):
    request, response = app.test_client.get("/get")
    assert request.args == {}
    assert response.text == "I am get method"