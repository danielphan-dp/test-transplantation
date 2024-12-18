import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.mark.parametrize('request_path', ['/test', '/another_test'])
def test_get_method(app: Sanic, request_path: str):
    @app.route(request_path, methods=["GET"])
    def get_route(request: Request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    
    assert response.status == 200
    assert response.text == 'I am get method'
    assert 'content-type' in response.headers
    assert response.headers['content-type'] == 'text/plain; charset=utf-8'