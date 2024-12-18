import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/post", methods=["POST"])
    async def post_handler(request):
        return text("I am post method")

    return app

@pytest.mark.asyncio
async def test_post_method(app):
    request, response = await app.test_client.post("/post")
    assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_method_with_data(app):
    request, response = await app.test_client.post("/post", data={"key": "value"})
    assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_method_invalid_route(app):
    request, response = await app.test_client.get("/post")
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text

@pytest.mark.asyncio
async def test_post_method_empty_body(app):
    request, response = await app.test_client.post("/post", data="")
    assert response.text == "I am post method"