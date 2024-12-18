import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.route("/", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    request, response = app.test_client.post("/")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_data(app):
    @app.route("/", methods=["POST"])
    async def handler(request):
        return text(request.json.get("key", "default"))

    request, response = app.test_client.post("/", json={"key": "value"})
    assert response.status == 200
    assert response.text == "value"

def test_post_method_empty_body(app):
    @app.route("/", methods=["POST"])
    async def handler(request):
        return text("Empty body received" if not request.body else "Body received")

    request, response = app.test_client.post("/")
    assert response.status == 200
    assert response.text == "Empty body received"

def test_post_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_post_method_method_not_allowed(app):
    @app.route("/", methods=["GET"])
    async def handler(request):
        return text("GET method")

    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text