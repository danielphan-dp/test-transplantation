import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers.get("Custom-Header") is None  # No custom header in response

def test_get_method_order_of_operations(app):
    operations = []

    @app.on_request
    async def on_request(_):
        operations.append(1)

    @app.on_response
    async def on_response(*_):
        operations.append(5)

    @app.get("/")
    async def handler(_):
        operations.append(3)
        return text('I am get method')

    @app.signal(Event.HTTP_HANDLER_BEFORE)
    async def handler_before(**_):
        operations.append(2)

    @app.signal(Event.HTTP_HANDLER_AFTER)
    async def handler_after(**_):
        operations.append(4)

    app.test_client.get("/")
    assert operations == [1, 2, 3, 4, 5]