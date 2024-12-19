import pytest
from sanic_testing.reusable import ReusableClient
from sanic.response import text

@pytest.fixture
def app():
    from sanic import Sanic
    app = Sanic("TestApp")

    @app.get("/")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method(app, port):
    client = ReusableClient(app, port=port)

    with client:
        _, response = client.get("/")
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app, port):
    client = ReusableClient(app, port=port)

    with client:
        _, response = client.get("/invalid")

    assert response.status == 404

def test_get_method_with_query_params(app, port):
    client = ReusableClient(app, port=port)

    with client:
        _, response = client.get("/?foo=bar")

    assert response.status == 200
    assert response.text == 'I am get method'