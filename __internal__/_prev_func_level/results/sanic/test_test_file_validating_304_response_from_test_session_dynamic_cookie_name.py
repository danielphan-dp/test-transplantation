import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url', ['/get', '/another_get'])
def test_get_method_response(app: Sanic, url: str):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, url)

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app: Sanic):
    request, response = app.test_client.get('/invalid_route')
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app: Sanic):
    class DummyView:
        def get(self, request):
            return text(f'Query param value: {request.args.get("param", "None")}')

    app.add_route(DummyView().get, '/query')

    request, response = app.test_client.get('/query?param=test')
    assert response.status == 200
    assert response.text == 'Query param value: test'