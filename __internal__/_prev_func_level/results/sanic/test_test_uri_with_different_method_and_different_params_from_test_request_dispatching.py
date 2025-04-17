import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/test_post", methods=["POST"])
    async def post_method(request):
        return text('I am post method')

    return app

@pytest.mark.asyncio
async def test_post_method_success(app):
    request, response = await app.test_client.post("/test_post")
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.asyncio
async def test_post_method_invalid_route(app):
    request, response = await app.test_client.get("/test_post")
    assert response.status == 405
    assert "Method GET not allowed for URL /test_post" in response.text

@pytest.mark.asyncio
async def test_post_method_with_data(app):
    request, response = await app.test_client.post("/test_post", data={"key": "value"})
    assert response.status == 200
    assert response.text == 'I am post method'  # Ensure the response remains the same regardless of data

@pytest.mark.asyncio
async def test_post_method_empty_body(app):
    request, response = await app.test_client.post("/test_post", data="")
    assert response.status == 200
    assert response.text == 'I am post method'  # Ensure the response remains the same with empty body

@pytest.mark.asyncio
async def test_post_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = await app.test_client.post("/test_post", headers=headers)
    assert response.status == 200
    assert response.text == 'I am post method'  # Ensure the response remains the same with custom headers