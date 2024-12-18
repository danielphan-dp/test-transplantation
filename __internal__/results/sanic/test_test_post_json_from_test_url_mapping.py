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

    payload = {"key": "value"}
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/post", data=json.dumps(payload), headers=headers
    )

    assert request.json.get("key") == "value"
    assert response.body == b"I am post method"

def test_post_empty_body(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    request, response = app.test_client.post("/post", data="", headers={})

    assert response.body == b"I am post method"

def test_post_invalid_json(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    payload = "{invalid_json}"
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/post", data=payload, headers=headers
    )

    assert response.status == 400  # Expecting a bad request due to invalid JSON

def test_post_with_query_params(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    payload = {"key": "value"}
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/post?param1=value1", data=json.dumps(payload), headers=headers
    )

    assert request.json.get("key") == "value"
    assert request.args.get("param1") == "value1"
    assert response.body == b"I am post method"