import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.reusable import ReusableClient

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    client = ReusableClient(app)

    with client:
        request, response = client.get("/get")

    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_multiple_requests(app):
    client = ReusableClient(app)

    with client:
        request1, response1 = client.get("/get")
        request2, response2 = client.get("/get")

    assert response1.status == response2.status == 200
    assert response1.text == response2.text

def test_get_method_with_different_connections(app):
    client = ReusableClient(app)

    with client:
        request1, response1 = client.get("/get")
        request2, response2 = client.get("/get")

    assert response1.status == response2.status == 200
    assert response1.text == response2.text
    assert request1.id != request2.id
    assert id(request1.conn_info) == id(request2.conn_info)