import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.reusable import ReusableClient

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    client = ReusableClient(app)

    with client:
        request, response = client.get("/")
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_multiple_requests(app):
    client = ReusableClient(app)

    with client:
        request1, response1 = client.get("/")
        request2, response2 = client.get("/")

    assert response1.status == response2.status == 200
    assert response1.text == response2.text == 'I am get method'
    assert request1.id != request2.id

def test_get_method_with_headers(app):
    client = ReusableClient(app)

    with client:
        request, response = client.get("/", headers={"X-Custom-Header": "value"})

    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers.get("X-Custom-Header") is None

def test_get_method_invalid_route(app):
    client = ReusableClient(app)

    with client:
        request, response = client.get("/invalid")

    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    client = ReusableClient(app)

    with client:
        request, response = client.get("/?foo=bar")

    assert response.status == 200
    assert response.text == 'I am get method'