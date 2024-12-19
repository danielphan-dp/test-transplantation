import json
from sanic import Sanic
from sanic.response import text
import pytest

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.post("/post")
    async def handler(request):
        return text("I am post method")

    payload = {"test": "data"}
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/post", data=json.dumps(payload), headers=headers
    )

    assert request.json.get("test") == "data"
    assert response.text == "I am post method"

def test_post_empty_payload(app):
    @app.post("/post")
    async def handler(request):
        return text("I am post method")

    payload = {}
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/post", data=json.dumps(payload), headers=headers
    )

    assert request.json == {}
    assert response.text == "I am post method"

def test_post_invalid_json(app):
    @app.post("/post")
    async def handler(request):
        return text("I am post method")

    payload = "{invalid_json}"
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/post", data=payload, headers=headers
    )

    assert response.status == 400  # Assuming the app returns 400 for invalid JSON

def test_post_with_special_characters(app):
    @app.post("/post")
    async def handler(request):
        return text("I am post method")

    payload = {"test": "✓"}
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/post", data=json.dumps(payload), headers=headers
    )

    assert request.json.get("test") == "✓"
    assert response.text == "I am post method"