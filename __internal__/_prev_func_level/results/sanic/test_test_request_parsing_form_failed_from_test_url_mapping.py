import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method_response(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_empty_body(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    request, response = app.test_client.post("/post", data="")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_invalid_content_type(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    headers = {"content-type": "text/plain"}
    request, response = app.test_client.post("/post", data="test", headers=headers)
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_logging_error(app, caplog):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        raise Exception("Test Exception")

    with caplog.at_level(logging.ERROR):
        request, response = app.test_client.post("/post")
    
    assert caplog.record_tuples[-1] == (
        "sanic.error",
        logging.ERROR,
        "Test Exception",
    )