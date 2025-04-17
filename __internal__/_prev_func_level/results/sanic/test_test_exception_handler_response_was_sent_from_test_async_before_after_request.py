import logging
from typing import Callable, List
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import ServerError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_exception(app, caplog: LogCaptureFixture, message_in_records: Callable[[List[logging.LogRecord], str], bool]):
    exception_handler_ran = False

    @app.exception(ServerError)
    async def exception_handler(request, exception):
        nonlocal exception_handler_ran
        exception_handler_ran = True
        return text("Error")

    @app.route("/get_with_error", methods=["GET"])
    async def get_method_with_error(request):
        raise ServerError("Exception")

    with caplog.at_level(logging.WARNING):
        request, response = app.test_client.get("/get_with_error")
        assert "Error" in response.text
        assert exception_handler_ran

    message_in_records(
        caplog.records,
        (
            "An error occurred while handling the request after at "
            "least some part of the response was sent to the client."
        ),
    )