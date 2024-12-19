import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/get")
async def get_handler(request):
    return text('I am get method')

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_non_str_headers(app):
    @app.route("/get_with_headers")
    async def handler(request):
        headers = {"answer": 42}
        return text("Hello", headers=headers)

    request, response = app.test_client.get("/get_with_headers")
    assert response.headers.get("answer") == "42"

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get", headers={})
    assert response.text == 'I am get method'

def test_get_method_with_query_params(app):
    @app.route("/get_with_query")
    async def query_handler(request):
        return text(f"Query param: {request.args.get('param')}")

    request, response = app.test_client.get("/get_with_query?param=test")
    assert response.text == "Query param: test"