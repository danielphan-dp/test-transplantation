import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path', ['/test', '/another_test'])
def test_get_method(app: Sanic, request_path: str):
    @app.route(request_path, methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'

    # Test with an invalid path
    request, response = app.test_client.get('/invalid_path')
    assert response.status == 404
    assert "Requested URL /invalid_path not found" in response.text

    # Test with a different method
    request, response = app.test_client.post(request_path)
    assert response.status == 405
    assert "Method POST not allowed for URL" in response.text