import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/", methods=["POST"])
    async def post(request):
        return text("I am post method")

    return app

@pytest.mark.asyncio
async def test_post_method_response(app):
    request, response = await app.asgi_client.post("/")
    assert response.status == 200
    assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_method_with_empty_body(app):
    request, response = await app.asgi_client.post("/", data="")
    assert response.status == 200
    assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_method_with_invalid_content_type(app):
    headers = {"Content-Type": "application/json"}
    request, response = await app.asgi_client.post("/", data="{}", headers=headers)
    assert response.status == 200
    assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_method_with_query_parameters(app):
    request, response = await app.asgi_client.post("/?param=value")
    assert response.status == 200
    assert response.text == "I am post method"