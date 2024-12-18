import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('file_name', ['test.file'])
def test_get_method(app: Sanic):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/get')

    request, response = app.test_client.get('/get')
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app: Sanic):
    request, response = app.test_client.get('/invalid_route')
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_middleware(app: Sanic):
    triggered = False

    @app.middleware("request")
    async def middleware(request):
        nonlocal triggered
        triggered = True

    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/get')

    request, response = app.test_client.get('/get')

    assert triggered is True
    assert response.status == 200
    assert response.text == 'I am get method'