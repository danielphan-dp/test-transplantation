import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url', ['/'])
def test_get_method_response(app, url):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, url)

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get('/invalid')
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param(app):
    class DummyView:
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'Param value is {param}')

    app.add_route(DummyView().get, '/query')

    request, response = app.test_client.get('/query?param=test')
    assert response.status == 200
    assert response.text == 'Param value is test'

    request, response = app.test_client.get('/query')
    assert response.status == 200
    assert response.text == 'Param value is default'