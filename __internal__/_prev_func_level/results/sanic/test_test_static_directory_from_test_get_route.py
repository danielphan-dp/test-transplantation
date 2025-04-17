import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('uri', ['/test', '/another_test'])
def test_get_method(app, uri):
    @app.get(uri)
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(uri)
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('invalid_uri', ['/invalid', '/not_found'])
def test_get_method_invalid_uri(app, invalid_uri):
    @app.get('/valid')
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(invalid_uri)
    assert response.status == 404
    assert "Requested URL" in response.text

def test_get_method_with_query_params(app):
    @app.get('/query')
    def handler(request):
        return text(f'I am get method with query param: {request.args.get("param")}')

    request, response = app.test_client.get('/query?param=test')
    assert response.status == 200
    assert response.text == 'I am get method with query param: test'