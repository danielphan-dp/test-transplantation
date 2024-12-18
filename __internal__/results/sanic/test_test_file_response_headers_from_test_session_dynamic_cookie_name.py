import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url', ['/get', '/get/'])
def test_get_method(app: Sanic, url: str):
    @app.route(url, methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(url)
    assert response.text == 'I am get method'
    assert response.status == 200

@pytest.mark.parametrize('url', ['/get', '/get/'])
def test_get_method_with_query_params(app: Sanic, url: str):
    @app.route(url, methods=["GET"])
    def get_method_with_query(request):
        return text(f'I am get method with query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get(f'{url}?param=test')
    assert response.text == 'I am get method with query param: test'
    assert response.status == 200

def test_get_method_not_found(app: Sanic):
    request, response = app.test_client.get('/nonexistent')
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_invalid_method(app: Sanic):
    @app.route('/get', methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.post('/get')
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text