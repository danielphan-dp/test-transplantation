import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_path', ['/get', '/another_get'])
def test_get_method(app, request_path):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, request_path)

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get('/invalid_route')
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_header(app):
    class DummyView:
        def get(self, request):
            return text('I am get method with custom header')

    app.add_route(DummyView().get, '/custom_header')

    headers = {'X-Custom-Header': 'value'}
    request, response = app.test_client.get('/custom_header', headers=headers)
    assert response.status == 200
    assert response.text == 'I am get method with custom header'
    assert response.headers['X-Custom-Header'] == 'value'  # Assuming the header is echoed back

def test_get_method_with_query_params(app):
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