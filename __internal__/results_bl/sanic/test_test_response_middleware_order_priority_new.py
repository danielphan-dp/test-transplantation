import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('expected', [
    'I am get method',
])
def test_get_method_response(app: Sanic, expected):
    @app.get("/test-get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/test-get")
    
    assert response.text == expected

@pytest.mark.parametrize('expected', [
    'I am get method',
])
def test_get_method_response_with_different_path(app: Sanic, expected):
    @app.get("/another-path")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/another-path")
    
    assert response.text == expected

@pytest.mark.parametrize('expected', [
    'I am get method',
])
def test_get_method_response_with_query_params(app: Sanic, expected):
    @app.get("/test-get-with-query")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/test-get-with-query?param=value")
    
    assert response.text == expected

@pytest.mark.parametrize('expected', [
    'I am get method',
])
def test_get_method_response_with_headers(app: Sanic, expected):
    @app.get("/test-get-with-headers")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/test-get-with-headers", headers={'Custom-Header': 'value'})
    
    assert response.text == expected