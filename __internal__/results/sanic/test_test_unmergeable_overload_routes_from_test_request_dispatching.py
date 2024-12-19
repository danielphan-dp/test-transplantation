import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import MethodNotAllowed

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.route("/post", methods=["POST"])
    async def post_handler(request):
        return text("I am post method")

    request, response = app.test_client.post("/post")
    assert response.text == "I am post method"

    request, response = app.test_client.get("/post")
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text

def test_post_method_with_data(app):
    @app.route("/post_data", methods=["POST"])
    async def post_data_handler(request):
        return text(request.json.get("key", "No key"))

    request, response = app.test_client.post("/post_data", json={"key": "value"})
    assert response.text == "value"

    request, response = app.test_client.post("/post_data", json={})
    assert response.text == "No key"

    request, response = app.test_client.get("/post_data")
    assert response.status == 405
    assert "Method GET not allowed for URL /post_data" in response.text

def test_post_method_invalid_route(app):
    @app.route("/invalid_post", methods=["POST"])
    async def invalid_post_handler(request):
        return text("This should not be reached")

    request, response = app.test_client.post("/non_existent_route")
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text