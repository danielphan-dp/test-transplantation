import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('path', ['/test', '/another_test'])
def test_get_method(app, path):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, path)
    request, response = app.test_client.get(path)
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get('/non_existent_path')
    assert response.status == 404
    assert "Requested URL /non_existent_path not found" in response.text

def test_get_method_with_query_param(app):
    class DummyView:
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'I am get method with param: {param}')

    app.add_route(DummyView().get, '/query_test')
    request, response = app.test_client.get('/query_test?param=test_value')
    
    assert response.status == 200
    assert response.text == 'I am get method with param: test_value'