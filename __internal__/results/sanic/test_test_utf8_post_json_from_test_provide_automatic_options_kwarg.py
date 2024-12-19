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

    request, response = app.test_client.post("/post")
    
    assert response.text == "I am post method"
    assert response.status == 200

def test_post_with_json_payload(app):
    @app.post("/post")
    async def handler(request):
        return text("Received: " + request.json.get("data", ""))

    payload = {"data": "test"}
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/post", data=json.dumps(payload), headers=headers
    )

    assert request.json.get("data") == "test"
    assert response.text == "Received: test"

def test_post_with_empty_payload(app):
    @app.post("/post")
    async def handler(request):
        return text("Received: " + request.json.get("data", "empty"))

    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/post", data=json.dumps({}), headers=headers
    )

    assert request.json.get("data") == None
    assert response.text == "Received: empty"

def test_post_method_not_allowed(app):
    @app.post("/post")
    async def handler(request):
        return text("I am post method")

    request, response = app.test_client.get("/post")
    
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text