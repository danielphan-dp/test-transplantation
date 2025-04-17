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
        _, response1 = client.get("/")
        _, response2 = client.get("/")

    assert response1.status == response2.status == 200
    assert response1.text == response2.text == 'I am get method'

def test_get_method_with_different_connections(app):
    client = ReusableClient(app)

    with client:
        _, response1 = client.get("/")
        _, response2 = client.get("/")

    assert response1.status == response2.status == 200
    assert response1.text == response2.text == 'I am get method'
    assert response1.json['request_id'] != response2.json['request_id']  # Assuming request_id is part of the response in a real scenario

def test_get_method_invalid_route(app):
    client = ReusableClient(app)

    with client:
        _, response = client.get("/invalid")

    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text  # Assuming this is the expected error message