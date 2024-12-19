import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/", methods=["GET"])
    async def get(request):
        return text("I am get method")
    return app

def test_get_method_response(app):
    request, _ = app.test_client.get("/")
    assert request.status == 200
    assert request.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, _ = app.test_client.get("/invalid")
    assert request.status == 404

def test_get_method_with_query_parameters(app):
    request, _ = app.test_client.get("/?param=value")
    assert request.status == 200
    assert request.text == "I am get method"  # Assuming the method does not change based on query params

def test_get_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, _ = app.test_client.get("/", headers=headers)
    assert request.status == 200
    assert request.text == "I am get method"  # Assuming the method does not change based on headers