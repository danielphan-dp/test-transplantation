import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url', ['/test', '/another_test'])
def test_get_method(app: Sanic, url):
    @app.route(url, methods=["GET"])
    def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app: Sanic):
    request, response = app.test_client.get('/invalid_route')
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_header(app: Sanic):
    @app.route("/custom_header", methods=["GET"])
    def custom_header_route(request):
        return text('I am get method', headers={'X-Custom-Header': 'value'})

    request, response = app.test_client.get('/custom_header')
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers['X-Custom-Header'] == 'value'