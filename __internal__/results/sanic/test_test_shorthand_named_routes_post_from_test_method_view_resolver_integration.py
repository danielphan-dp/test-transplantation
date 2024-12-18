import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.post("/post")
    async def post_handler(request):
        return text("I am post method")

    return app

@pytest.mark.asyncio
async def test_post_method(app):
    request, response = await app.asgi_client.post("/post")
    assert response.text == "I am post method"
    assert response.status == 200

@pytest.mark.asyncio
async def test_post_method_invalid_route(app):
    request, response = await app.asgi_client.post("/invalid")
    assert response.status == 404

@pytest.mark.asyncio
async def test_post_method_with_data(app):
    data = {"key": "value"}
    request, response = await app.asgi_client.post("/post", json=data)
    assert response.text == "I am post method"
    assert response.status == 200

@pytest.mark.asyncio
async def test_post_method_empty_body(app):
    request, response = await app.asgi_client.post("/post", json={})
    assert response.text == "I am post method"
    assert response.status == 200

@pytest.mark.asyncio
async def test_post_method_with_invalid_json(app):
    request, response = await app.asgi_client.post("/post", data="invalid json")
    assert response.status == 400  # Assuming the app returns 400 for bad requests

@pytest.mark.asyncio
async def test_post_method_route_name(app):
    assert app.router.routes_all[("post",)].name is None  # No name assigned
    app.router.routes_all[("post",)].name = "post_route"
    assert app.url_for("post_route") == "/post"