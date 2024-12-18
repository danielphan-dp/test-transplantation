import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url', ['/'])
def test_get_method_response(app: Sanic, url: str):
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app: Sanic):
    request, response = app.test_client.get('/invalid')
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app: Sanic):
    @app.get("/query")
    async def query_handler(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get('/query?param=test')
    assert response.status == 200
    assert response.text == "Query param: test"

def test_get_method_with_headers(app: Sanic):
    @app.get("/headers")
    async def headers_handler(request):
        return text(f"Header value: {request.headers.get('X-Custom-Header', 'not set')}")

    request, response = app.test_client.get('/headers', headers={'X-Custom-Header': 'value'})
    assert response.status == 200
    assert response.text == "Header value: value"