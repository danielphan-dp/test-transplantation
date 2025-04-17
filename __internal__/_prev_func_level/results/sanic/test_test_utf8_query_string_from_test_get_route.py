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
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_query_string(app):
    request, response = app.test_client.get("/", params=[("query", "test")])
    assert response.status == 200
    assert response.text == "I am get method"
    assert request.args.get("query") == "test"

def test_get_method_with_empty_query_string(app):
    request, response = app.test_client.get("/", params=[("query", "")])
    assert response.status == 200
    assert response.text == "I am get method"
    assert request.args.get("query") == ""

def test_get_method_with_non_utf8_query_string(app):
    request, response = app.test_client.get("/", params=[("query", "😊")])
    assert response.status == 200
    assert response.text == "I am get method"
    assert request.args.get("query") == "😊"