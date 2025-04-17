import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.mark.asyncio
async def test_post_method(app):
    @app.route("/test_post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    request, response = await app.test_client.post("/test_post")
    assert response.status == 200
    assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_method_not_allowed(app):
    @app.route("/test_post", methods=["GET"])
    async def handler(request):
        return text("OK")

    request, response = await app.test_client.get("/test_post")
    assert response.status == 200

    request, response = await app.test_client.post("/test_post")
    assert response.status == 405

@pytest.mark.asyncio
async def test_post_with_invalid_route(app):
    request, response = await app.test_client.post("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

@pytest.mark.asyncio
async def test_post_with_empty_body(app):
    @app.route("/test_post_empty", methods=["POST"])
    async def handler(request):
        return text("Received empty body" if not request.body else "Received body")

    request, response = await app.test_client.post("/test_post_empty", data="")
    assert response.status == 200
    assert response.text == "Received empty body"