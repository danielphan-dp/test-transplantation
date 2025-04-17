import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url', ['/'])
def test_get_method(app: Sanic, url: str):
    @app.route(url, methods=["GET"])
    def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('url', ['/'])
def test_get_method_with_invalid_header(app: Sanic, url: str):
    @app.route(url, methods=["GET"])
    def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get(url, headers={"invalid-header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('url', ['/'])
def test_get_method_with_empty_header(app: Sanic, url: str):
    @app.route(url, methods=["GET"])
    def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get(url, headers={"if-modified-since": ""})
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('url', ['/'])
def test_get_method_with_nonexistent_route(app: Sanic, url: str):
    request, response = app.test_client.get('/nonexistent')
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text