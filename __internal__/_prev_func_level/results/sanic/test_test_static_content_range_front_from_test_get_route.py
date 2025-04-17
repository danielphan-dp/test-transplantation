import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('path', ['/test', '/another_test'])
def test_get_method(app, path):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, path)

    request, response = app.test_client.get(path)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get('/invalid_route')
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_header(app):
    class DummyView:
        def get(self, request):
            return text('I am get method', headers={'X-Custom-Header': 'value'})

    app.add_route(DummyView().get, '/custom_header')

    request, response = app.test_client.get('/custom_header')
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers['X-Custom-Header'] == 'value'