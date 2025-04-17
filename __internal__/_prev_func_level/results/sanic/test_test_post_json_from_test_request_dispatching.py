import json
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    payload = {"test": "OK"}
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/post", data=json.dumps(payload), headers=headers
    )

    assert request.json.get("test") == "OK"
    assert response.body == b"I am post method"

def test_post_empty_payload(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/post", data=json.dumps({}), headers=headers
    )

    assert request.json == {}
    assert response.body == b"I am post method"

def test_post_invalid_json(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/post", data="invalid json", headers=headers
    )

    assert response.status == 400  # Assuming the app returns 400 for invalid JSON

def test_post_method_with_different_content_type(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    payload = "test=OK"
    headers = {"content-type": "application/x-www-form-urlencoded"}

    request, response = app.test_client.post(
        "/post", data=payload, headers=headers
    )

    assert request.form.get("test") == "OK"
    assert response.body == b"I am post method"