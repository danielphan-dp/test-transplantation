import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.reusable import ReusableClient

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    client = ReusableClient(app)
    with client:
        _, response = client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_large_header(app):
    client = ReusableClient(app)
    large_header = {"X-Large-Header": "x" * 10_000}
    with client:
        _, response = client.get("/", headers=large_header)
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_empty_request(app):
    client = ReusableClient(app)
    with client:
        _, response = client.get("/", headers={})
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_method(app):
    client = ReusableClient(app)
    with client:
        _, response = client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text