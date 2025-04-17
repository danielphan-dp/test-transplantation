import json
from sanic import Sanic
from sanic.response import text
import pytest

@pytest.fixture
def app():
    return Sanic(name="Test")

@pytest.mark.asyncio
async def test_post_method(app):
    @app.route("/post", methods=["POST"])
    async def post_handler(request):
        return text("I am post method")

    payload = {"TEST": "OK"}
    headers = {"content-type": "application/json"}

    request, response = await app.test_client.post(
        "/post", data=json.dumps(payload), headers=headers
    )

    assert request.body == b'{"TEST": "OK"}'
    assert request.json.get("TEST") == "OK"
    assert response.text == "I am post method"
    assert response.status == 200

@pytest.mark.asyncio
async def test_post_empty_body(app):
    @app.route("/post", methods=["POST"])
    async def post_handler(request):
        return text("I am post method")

    request, response = await app.test_client.post("/post", data="", headers={})

    assert request.body == b""
    assert response.text == "I am post method"
    assert response.status == 200

@pytest.mark.asyncio
async def test_post_invalid_json(app):
    @app.route("/post", methods=["POST"])
    async def post_handler(request):
        return text("I am post method")

    payload = "{invalid_json}"
    headers = {"content-type": "application/json"}

    request, response = await app.test_client.post(
        "/post", data=payload, headers=headers
    )

    assert response.status == 400  # Assuming the app returns 400 for bad JSON
    assert "Invalid JSON" in response.text  # Adjust based on actual error message

@pytest.mark.asyncio
async def test_post_method_with_query_params(app):
    @app.route("/post", methods=["POST"])
    async def post_handler(request):
        return text("I am post method")

    payload = {"TEST": "OK"}
    headers = {"content-type": "application/json"}

    request, response = await app.test_client.post(
        "/post?param=value", data=json.dumps(payload), headers=headers
    )

    assert request.body == b'{"TEST": "OK"}'
    assert request.json.get("TEST") == "OK"
    assert response.text == "I am post method"
    assert response.status == 200