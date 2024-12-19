import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_method', ['GET', 'POST'])
def test_get_method_response(app, request_method):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/get')

    if request_method == 'GET':
        request, response = app.test_client.get('/get')
    else:
        request, response = app.test_client.post('/get')

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
            return text(f'Param value is {param}')

    app.add_route(DummyView().get, '/get_with_param')

    request, response = app.test_client.get('/get_with_param?param=test_value')
    assert response.status == 200
    assert response.text == 'Param value is test_value'

    request, response = app.test_client.get('/get_with_param')
    assert response.status == 200
    assert response.text == 'Param value is default'