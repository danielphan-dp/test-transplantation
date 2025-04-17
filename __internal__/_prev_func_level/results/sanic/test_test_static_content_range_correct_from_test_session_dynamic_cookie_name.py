import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_path', ['/test', '/another_test'])
def test_get_method(app, request_path):
    @app.route(request_path)
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get('/invalid_route')
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.route('/query_test')
    def get_with_query(request):
        return text(f"Query param: {request.args.get('param', 'None')}")

    request, response = app.test_client.get('/query_test?param=value')
    assert response.status == 200
    assert response.text == "Query param: value"