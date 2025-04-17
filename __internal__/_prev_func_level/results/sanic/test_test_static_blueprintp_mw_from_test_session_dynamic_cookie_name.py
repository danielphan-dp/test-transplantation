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
    
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_middleware(app: Sanic):
    results = []

    @app.middleware("request")
    async def process_request(request):
        results.append(request)

    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/get')

    request, response = app.test_client.get('/get')

    assert response.text == 'I am get method'
    assert type(results[0]) is request.__class__
    assert response.status == 200

def test_get_method_not_found(app: Sanic):
    request, response = app.test_client.get('/nonexistent')
    
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_invalid_method(app: Sanic):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/get')

    request, response = app.test_client.post('/get')
    
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text