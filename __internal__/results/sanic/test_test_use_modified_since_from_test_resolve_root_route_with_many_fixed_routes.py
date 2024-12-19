import os
import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png'])
def test_get_method_response(app, file_name):
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

def test_get_method_with_custom_header(app):
    class DummyView:
        def get(self, request):
            return text('I am get method with custom header')

    app.add_route(DummyView().get, '/custom-header')

    request, response = app.test_client.get('/custom-header', headers={'Custom-Header': 'value'})

    assert response.status == 200
    assert response.text == 'I am get method with custom header'