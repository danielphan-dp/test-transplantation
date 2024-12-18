import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/")
    async def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/", params={"param1": "value1", "param2": "value2"})
    assert response.text == "I am get method"
    assert request.args.get("param1") == "value1"
    assert request.args.get("param2") == "value2"

def test_get_method_with_no_params(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert request.args == {}

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_multiple_requests(app):
    for _ in range(10):
        request, response = app.test_client.get("/")
        assert response.text == "I am get method"
        assert response.status == 200