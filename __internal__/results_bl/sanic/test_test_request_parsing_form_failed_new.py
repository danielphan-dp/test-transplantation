import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/", methods=["POST"])
    async def handler(request):
        return text("I am post method")
    return app

def test_post_method_success(app):
    payload = "test=OK"
    headers = {"content-type": "application/x-www-form-urlencoded"}

    request, response = app.test_client.post("/", data=payload, headers=headers)

    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_empty_payload(app):
    payload = ""
    headers = {"content-type": "application/x-www-form-urlencoded"}

    request, response = app.test_client.post("/", data=payload, headers=headers)

    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_invalid_content_type(app):
    payload = "test=OK"
    headers = {"content-type": "text/plain"}

    request, response = app.test_client.post("/", data=payload, headers=headers)

    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_caplog(app, caplog):
    payload = "test=OK"
    headers = {"content-type": "multipart/form-data"}

    with caplog.at_level(logging.ERROR):
        request, response = app.test_client.post("/", data=payload, headers=headers)

    assert caplog.record_tuples[-1] == (
        "sanic.error",
        logging.ERROR,
        "Failed when parsing form",
    )