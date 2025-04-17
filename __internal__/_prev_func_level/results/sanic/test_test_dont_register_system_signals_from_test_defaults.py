import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.mark.skipif(os.name == 'nt', reason='May hang CI on py38/windows')
def test_get_method(app):
    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/get_with_header")
    async def get_method_with_header(request):
        return text('I am get method with custom header')

    request, response = app.test_client.get("/get_with_header", headers={"X-Custom-Header": "value"})
    assert response.text == 'I am get method with custom header'
    assert response.status == 200
    assert response.headers.get("X-Custom-Header") is None  # Ensure the header is not returned in the response

def test_get_method_with_query_params(app):
    @app.get("/get_with_query")
    async def get_method_with_query(request):
        param = request.args.get('param', 'default')
        return text(f'Query param is {param}')

    request, response = app.test_client.get("/get_with_query?param=test")
    assert response.text == 'Query param is test'
    assert response.status == 200

    request, response = app.test_client.get("/get_with_query")
    assert response.text == 'Query param is default'
    assert response.status == 200