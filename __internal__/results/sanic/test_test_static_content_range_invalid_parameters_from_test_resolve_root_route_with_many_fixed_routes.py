import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_path', ['/valid_path', '/another_valid_path'])
def test_get_method_valid_paths(app, request_path):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, request_path)

    request, response = app.test_client.get(request_path)

    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_path(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/valid_path')

    request, response = app.test_client.get('/invalid_path')

    assert response.status == 404
    assert "Requested URL /invalid_path not found" in response.text

def test_get_method_with_query_params(app):
    class DummyView:
        def get(self, request):
            return text(f'I am get method with query param: {request.args.get("param")}')

    app.add_route(DummyView().get, '/query')

    request, response = app.test_client.get('/query?param=test')

    assert response.status == 200
    assert response.text == 'I am get method with query param: test'