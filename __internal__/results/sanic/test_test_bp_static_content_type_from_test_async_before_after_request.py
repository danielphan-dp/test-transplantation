import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.mark.parametrize('url', ['/get', '/another_get'])
def test_get_method(app, url):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, url)

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get('/non_existent_route')
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_method_with_query_params(app):
    class DummyView:
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'Param value is {param}')

    app.add_route(DummyView().get, '/get_with_param')

    request, response = app.test_client.get('/get_with_param?param=test')
    assert response.status == 200
    assert response.text == 'Param value is test'

    request, response = app.test_client.get('/get_with_param')
    assert response.status == 200
    assert response.text == 'Param value is default'