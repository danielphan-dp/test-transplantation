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

def test_get_method_response(app):
    client = ReusableClient(app)
    
    with client:
        _, response = client.get("/")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_bad_headers(app):
    client = ReusableClient(app)
    bad_headers = {"bad": "bad" * 5_000}

    with client:
        _, response1 = client.get("/")
        _, response2 = client.get("/", headers=bad_headers)

    assert response1.status == 200
    assert response2.status == 413
    assert response1.headers["x-request-id"] != response2.headers["x-request-id"]

def test_get_method_with_query_params(app):
    @app.get("/query")
    async def query_handler(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    client = ReusableClient(app)

    with client:
        _, response = client.get("/query?param=test")

    assert response.status == 200
    assert response.text == "Query param: test"

def test_get_method_with_empty_query_params(app):
    @app.get("/query")
    async def query_handler(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    client = ReusableClient(app)

    with client:
        _, response = client.get("/query?param=")

    assert response.status == 200
    assert response.text == "Query param: none"