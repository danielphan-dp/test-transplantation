import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_method(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/get')

    request, response = app.test_client.get('/get')
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_request(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/get')

    request, response = app.test_client.get('/get', headers={'Invalid-Header': 'value'})
    
    assert response.status == 200
    assert response.text == 'I am get method'