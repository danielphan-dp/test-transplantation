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

    payload = "test=OK"
    headers = {"content-type": "application/x-www-form-urlencoded"}

    request, response = app.test_client.post(
        "/post", data=payload, headers=headers
    )

    assert response.status == 200
    assert response.text == "I am post method"
    assert request.form.get("test") == "OK"

def test_post_empty_payload(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    payload = ""
    headers = {"content-type": "application/x-www-form-urlencoded"}

    request, response = app.test_client.post(
        "/post", data=payload, headers=headers
    )

    assert response.status == 200
    assert response.text == "I am post method"
    assert request.form.get("test") is None

def test_post_invalid_content_type(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    payload = "test=OK"
    headers = {"content-type": "text/plain"}

    request, response = app.test_client.post(
        "/post", data=payload, headers=headers
    )

    assert response.status == 200
    assert response.text == "I am post method"
    assert request.form.get("test") is None

def test_post_with_blank_values(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    payload = "test="
    headers = {"content-type": "application/x-www-form-urlencoded"}

    request, response = app.test_client.post(
        "/post", data=payload, headers=headers
    )

    assert response.status == 200
    assert response.text == "I am post method"
    assert request.form.get("test") == ""