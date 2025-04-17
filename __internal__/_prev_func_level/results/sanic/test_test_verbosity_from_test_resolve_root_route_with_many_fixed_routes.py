import logging
import uuid
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('app_verbosity,log_verbosity,exists', [
    (0, 0, True), 
    (0, 1, False), 
    (0, 2, False), 
    (1, 0, True), 
    (1, 1, True), 
    (1, 2, False), 
    (2, 0, True), 
    (2, 1, True), 
    (2, 2, True)
])
def test_get_method_logging(app, caplog, app_verbosity, log_verbosity, exists):
    rand_string = str(uuid.uuid4())

    @app.get("/")
    def get_method(request):
        logger.info("DEFAULT")
        logger.info(rand_string, extra={"verbosity": log_verbosity})
        return text("I am get method")

    with caplog.at_level(logging.INFO):
        _ = app.test_client.get("/", server_kwargs={"verbosity": app_verbosity})

    record = ("sanic.root", logging.INFO, rand_string)

    if exists:
        assert record in caplog.record_tuples
    else:
        assert record not in caplog.record_tuples

    if app_verbosity == 0:
        assert ("sanic.root", logging.INFO, "DEFAULT") in caplog.record_tuples

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"