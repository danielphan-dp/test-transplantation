import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('url', ['/'])
def test_get_method(app: Sanic, url):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, url)

    request, response = app.test_client.get(url)

    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('url', ['/nonexistent'])
def test_get_method_not_found(app: Sanic, url):
    request, response = app.test_client.get(url)

    assert response.status == 404
    assert "Requested URL" in response.text

@pytest.mark.parametrize('url', ['/'])
def test_get_method_with_middleware(app: Sanic, url):
    results = []

    @app.middleware("request")
    async def middleware(request):
        results.append(request)

    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, url)

    request, response = app.test_client.get(url)

    assert response.text == 'I am get method'
    assert len(results) == 1
    assert results[0] == request

@pytest.mark.parametrize('url', ['/'])
def test_get_method_with_custom_response(app: Sanic, url):
    class DummyView:
        def get(self, request):
            return text('Custom response', status=201)

    app.add_route(DummyView().get, url)

    request, response = app.test_client.get(url)

    assert response.status == 201
    assert response.text == 'Custom response'