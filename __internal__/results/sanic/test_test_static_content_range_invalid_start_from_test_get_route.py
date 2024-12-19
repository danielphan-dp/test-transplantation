import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url', ['/test', '/another_test'])
def test_get_method(app, url):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, url)

    request, response = app.test_client.get(url)

    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get('/invalid_route')

    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    class DummyView:
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'I am get method with param: {param}')

    app.add_route(DummyView().get, '/query_test')

    request, response = app.test_client.get('/query_test?param=test_value')

    assert response.status == 200
    assert response.text == 'I am get method with param: test_value'