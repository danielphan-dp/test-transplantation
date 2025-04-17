import json
import pytest
from sanic import Sanic
from sanic.response import text

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
        return text(request.json.get("message", "No message"))

    payload = {"message": "Hello, World!"}
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/post", data=json.dumps(payload), headers=headers
    )

    assert request.json.get("message") == "Hello, World!"
    assert response.text == "Hello, World!"
    assert response.status == 200

def test_post_with_empty_payload(app):
    @app.post("/post")
    async def handler(request):
        return text("Empty payload")

    request, response = app.test_client.post("/post", data={})

    assert response.text == "Empty payload"
    assert response.status == 200

def test_post_method_not_allowed(app):
    @app.post("/post")
    async def handler(request):
        return text("I am post method")

    request, response = app.test_client.get("/post")

    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text

def test_post_with_form_urlencoded(app):
    @app.post("/post")
    async def handler(request):
        return text(request.form.get("test", "No test"))

    payload = "test=FormData"
    headers = {"content-type": "application/x-www-form-urlencoded"}

    request, response = app.test_client.post(
        "/post", data=payload, headers=headers
    )

    assert request.form.get("test") == "FormData"
    assert response.text == "FormData"
    assert response.status == 200