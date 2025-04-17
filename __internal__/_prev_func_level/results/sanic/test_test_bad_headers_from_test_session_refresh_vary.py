import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.reusable import ReusableClient

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    client = ReusableClient(app)
    with client:
        _, response = client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_bad_headers(app):
    client = ReusableClient(app)
    bad_headers = {"bad": "bad" * 5_000}
    with client:
        _, response = client.get("/get", headers=bad_headers)
    assert response.status == 413

def test_get_method_response_id(app):
    @app.on_response
    async def reqid(request, response):
        response.headers["x-request-id"] = request.id

    client = ReusableClient(app)
    with client:
        _, response1 = client.get("/get")
        _, response2 = client.get("/get")
    
    assert response1.headers["x-request-id"] != response2.headers["x-request-id"]