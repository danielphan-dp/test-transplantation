import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_content_type(app):
    request, response = app.test_client.get("/")
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param(app):
    @app.get("/query")
    async def get_with_query(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/query?param=test")
    assert response.text == 'Query param: test'