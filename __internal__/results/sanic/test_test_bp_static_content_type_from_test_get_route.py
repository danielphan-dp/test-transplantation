import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('url', ['/'])
def test_get_method_response(app, url):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, url)

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('url', ['/nonexistent'])
def test_get_method_not_found(app, url):
    request, response = app.test_client.get(url)
    assert response.status == 404
    assert "Requested URL" in response.text

@pytest.mark.parametrize('url', ['/'])
def test_get_method_with_custom_header(app, url):
    class DummyView:
        def get(self, request):
            return text('I am get method', headers={'X-Custom-Header': 'value'})

    app.add_route(DummyView().get, url)

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.headers['X-Custom-Header'] == 'value'