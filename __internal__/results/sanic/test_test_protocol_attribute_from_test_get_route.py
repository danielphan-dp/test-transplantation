import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get(request: Request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/", headers=headers)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # Assuming the method does not change based on query params

def test_get_method_protocol(app):
    retrieved = None

    @app.get("/protocol")
    async def get_protocol(request):
        nonlocal retrieved
        retrieved = request.protocol
        return text('Protocol retrieved')

    request, response = app.test_client.get("/protocol")
    assert response.status == 200
    assert retrieved is not None
    assert isinstance(retrieved, str)  # Assuming protocol is a string representation