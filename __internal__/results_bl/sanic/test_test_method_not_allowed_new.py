import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/test", methods=["POST"])
    async def post_handler(request):
        return text("I am post method")

    return app

@pytest.mark.asyncio
async def test_post_method_success(app):
    request, response = app.test_client.post("/test")
    assert response.status == 200
    assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_method_not_allowed(app):
    @app.route("/test", methods=["GET"])
    async def handler(request):
        return text("OK")

    request, response = app.test_client.get("/test")
    assert response.status == 200

    request, response = app.test_client.post("/test")
    assert response.status == 405

@pytest.mark.asyncio
async def test_post_method_empty_body(app):
    request, response = app.test_client.post("/test", data="")
    assert response.status == 200
    assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_method_with_json(app):
    request, response = app.test_client.post("/test", json={"key": "value"})
    assert response.status == 200
    assert response.text == "I am post method"