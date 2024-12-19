import json
from sanic import Sanic
from sanic.response import text
import pytest

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.post("/")
    async def handler(request):
        return text("I am post method")

    return app

def test_post_method(app):
    payload = {"key": "value"}
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/", data=json.dumps(payload), headers=headers
    )

    assert request.json.get("key") == "value"
    assert response.text == "I am post method"

def test_post_empty_json(app):
    payload = {}
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/", data=json.dumps(payload), headers=headers
    )

    assert request.json == {}
    assert response.text == "I am post method"

def test_post_invalid_json(app):
    payload = "invalid json"
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/", data=payload, headers=headers
    )

    assert response.status == 400  # Assuming the app returns 400 for invalid JSON

def test_post_with_special_characters(app):
    payload = {"test": "✓"}
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/", data=json.dumps(payload), headers=headers
    )

    assert request.json.get("test") == "✓"
    assert response.text == "I am post method"