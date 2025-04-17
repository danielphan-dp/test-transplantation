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

def test_post_method_with_invalid_data(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    payload = "invalid_data"
    headers = {"content-type": "application/x-www-form-urlencoded"}

    request, response = app.test_client.post("/post", data=payload, headers=headers)
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_logging_error(app, caplog):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        raise Exception("Simulated error")

    with caplog.at_level(logging.ERROR):
        request, response = app.test_client.post("/post")
    
    assert caplog.record_tuples[-1] == (
        "sanic.error",
        logging.ERROR,
        "Simulated error",
    )