import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or platform.system() == 'Windows', reason='Not testable with current client')
def test_get_method_response(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/get')

    request, response = app.test_client.get('/get')
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get('/invalid_route')
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_headers(app):
    class DummyView:
        def get(self, request):
            return text('I am get method with headers')

    app.add_route(DummyView().get, '/get_with_headers')

    headers = {"Custom-Header": "Test"}
    request, response = app.test_client.get('/get_with_headers', headers=headers)
    assert response.status == 200
    assert response.text == 'I am get method with headers'
    assert request.headers.get("Custom-Header") == "Test"