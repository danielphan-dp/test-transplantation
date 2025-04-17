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
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_not_allowed(app):
    @app.route("/post", methods=["GET"])
    async def get_handler(request):
        return text("OK")

    request, response = app.test_client.get("/post")
    assert response.status == 200

    request, response = app.test_client.post("/post")
    assert response.status == 405

def test_post_with_invalid_route(app):
    request, response = app.test_client.post("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_post_with_data(app):
    @app.route("/data", methods=["POST"])
    async def data_handler(request):
        return text(request.json.get("key", "default"))

    request, response = app.test_client.post("/data", json={"key": "value"})
    assert response.status == 200
    assert response.text == "value"

    request, response = app.test_client.post("/data", json={})
    assert response.status == 200
    assert response.text == "default"