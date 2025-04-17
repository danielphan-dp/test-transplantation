import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path', ['/get', '/another_get'])
def test_get_method(app: Sanic, request_path: str):
    @app.route(request_path, methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'

    # Test for non-existing route
    request, response = app.test_client.get('/non_existing_route')
    assert response.status == 404

    # Test for method not allowed
    request, response = app.test_client.post(request_path)
    assert response.status == 405
    assert "Method POST not allowed for URL" in response.text

    # Test for headers
    request, response = app.test_client.get(request_path)
    assert 'content-type' in response.headers
    assert response.headers['content-type'] == 'text/plain; charset=utf-8'