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
    headers = {"content-type": "application/xml"}
    request, response = await app.asgi_client.post("/", data="<data></data>", headers=headers)
    assert response.status == 200
    assert response.text == "I am post method"

@pytest.mark.asyncio
async def test_post_method_with_json_payload(app):
    payload = '{"key": "value"}'
    headers = {"content-type": "application/json"}
    request, response = await app.asgi_client.post("/", data=payload, headers=headers)
    assert response.status == 200
    assert response.text == "I am post method"