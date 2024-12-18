import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method_response(app):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text("I am post method")

    request, response = app.test_client.post("/")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_invalid_data(app):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text("I am post method")

    request, response = app.test_client.post("/", data="invalid data")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_logging(app, caplog):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text("I am post method")

    with caplog.at_level(logging.DEBUG):
        request, response = app.test_client.post("/")
    
    assert caplog.record_tuples[-1] == (
        "sanic.root",
        logging.DEBUG,
        "I am post method"
    )