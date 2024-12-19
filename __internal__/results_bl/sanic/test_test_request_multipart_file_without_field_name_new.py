import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/", methods=["POST"])
    async def post(request):
        return text("I am post method")
    return app

def test_post_method_response(app):
    request, _ = app.test_client.post("/")
    assert request.status == 200
    assert request.text == "I am post method"

def test_post_method_with_empty_body(app):
    request, _ = app.test_client.post("/", data="")
    assert request.status == 200
    assert request.text == "I am post method"

def test_post_method_with_invalid_content_type(app):
    headers = {"content-type": "text/plain"}
    request, _ = app.test_client.post("/", headers=headers)
    assert request.status == 200
    assert request.text == "I am post method"

def test_post_method_with_json_payload(app):
    payload = '{"key": "value"}'
    headers = {"content-type": "application/json"}
    request, _ = app.test_client.post("/", data=payload, headers=headers)
    assert request.status == 200
    assert request.text == "I am post method"

def test_post_method_logging(app, caplog):
    with caplog.at_level(logging.DEBUG):
        request, _ = app.test_client.post("/")
    assert caplog.record_tuples[-1] == (
        "sanic.root",
        logging.DEBUG,
        "I am post method"
    )