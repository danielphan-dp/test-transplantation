import pytest
from sanic import Sanic
from sanic.response import text

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
    assert response.status == 200

def test_post_method_invalid_method(app):
    @app.route("/post", methods=["POST"])
    async def post_handler(request):
        return text("I am post method")

    request, response = app.test_client.get("/post")
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text

def test_post_method_with_data(app):
    @app.route("/post_data", methods=["POST"])
    async def post_data_handler(request):
        return text(request.json.get("key", "No key"))

    request, response = app.test_client.post("/post_data", json={"key": "value"})
    assert response.text == "value"
    assert response.status == 200

def test_post_method_with_empty_data(app):
    @app.route("/post_empty", methods=["POST"])
    async def post_empty_handler(request):
        return text("Empty data received")

    request, response = app.test_client.post("/post_empty", json={})
    assert response.text == "Empty data received"
    assert response.status == 200

def test_post_method_with_invalid_json(app):
    @app.route("/post_invalid_json", methods=["POST"])
    async def post_invalid_json_handler(request):
        return text("Invalid JSON")

    request, response = app.test_client.post("/post_invalid_json", data="not a json")
    assert response.status == 400
    assert "Invalid JSON" in response.text