import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('param', ['test_param', 'another_param'])
def test_get_method_response(app, param):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/get')

    request, response = app.test_client.get('/get')

    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('invalid_param', [None, '', 'invalid'])
def test_get_method_with_invalid_param(app, invalid_param):
    class DummyView:
        def get(self, request, param):
            if param is None or param == '':
                return text('Invalid parameter', status=400)
            return text('I am get method')

    app.add_route(DummyView().get, '/get/<param>')

    request, response = app.test_client.get(f'/get/{invalid_param}')

    assert response.status == 400
    assert response.text == 'Invalid parameter'