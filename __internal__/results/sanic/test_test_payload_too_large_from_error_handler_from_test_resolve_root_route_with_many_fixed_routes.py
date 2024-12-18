import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import PayloadTooLarge

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.route("/get", methods=["GET"])
    async def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_payload_too_large(app):
    app.config.REQUEST_MAX_SIZE = 1

    @app.route("/large_payload", methods=["GET"])
    async def large_payload_handler(request):
        return text("OK")

    @app.exception(PayloadTooLarge)
    def handler_exception(request, exception):
        return text("Payload Too Large from error_handler.", 413)

    _, response = app.test_client.get("/large_payload", gather_request=False)
    assert response.status == 413
    assert response.text == "Payload Too Large from error_handler."