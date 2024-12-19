import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.reusable import ReusableClient

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method_success(app, port):
    client = ReusableClient(app, port=port)

    with client:
        _, response = client.get("/get")

    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app, port):
    client = ReusableClient(app, port=port)

    with client:
        _, response = client.get("/invalid")

    assert response.status == 404

def test_get_method_with_headers(app, port):
    client = ReusableClient(app, port=port)
    headers = {"Custom-Header": "value"}

    with client:
        _, response = client.get("/get", headers=headers)

    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers.get("Custom-Header") is None

def test_get_method_large_request(app, port):
    client = ReusableClient(app, port=port)
    large_data = "x" * 10_000

    with client:
        _, response = client.get("/get", headers={"Content-Length": str(len(large_data))})

    assert response.status == 200
    assert response.text == 'I am get method'