import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('uri', ['/test', '/another_test'])
def test_get_method(app, uri):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, uri)

    request, response = app.test_client.get(uri)
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('invalid_uri', ['/invalid', '/not_found'])
def test_get_method_invalid_uri(app, invalid_uri):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/valid')

    request, response = app.test_client.get(invalid_uri)
    assert response.status == 404
    assert "Requested URL" in response.text

def test_get_method_with_query_params(app):
    class DummyView:
        def get(self, request):
            return text(f'I am get method with query param: {request.args.get("param")}')

    app.add_route(DummyView().get, '/query')

    request, response = app.test_client.get('/query?param=test')
    assert response.status == 200
    assert response.text == 'I am get method with query param: test'