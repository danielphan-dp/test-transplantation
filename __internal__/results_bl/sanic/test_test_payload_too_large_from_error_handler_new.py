import pytest
from sanic import Sanic
from sanic.exceptions import PayloadTooLarge
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    app.config.REQUEST_MAX_SIZE = 1

    @app.route("/1")
    async def handler1(request):
        return text("OK")

    @app.exception(PayloadTooLarge)
    def handler_exception(request, exception):
        return text("Payload Too Large from error_handler.", 413)

    return app

def test_get_method(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_payload_too_large(app):
    app.config.REQUEST_MAX_SIZE = 1

    _, response = app.test_client.post("/1", data='x' * 2, gather_request=False)
    assert response.status == 413
    assert response.text == "Payload Too Large from error_handler."

def test_get_method_with_large_payload(app):
    app.config.REQUEST_MAX_SIZE = 1

    _, response = app.test_client.get("/get", data='x' * 2, gather_request=False)
    assert response.status == 200
    assert response.text == 'I am get method'