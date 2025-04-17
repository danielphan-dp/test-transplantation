import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('path, expected_response', [
    ('/get', 'I am get method'),
    ('/nonexistent', 'Not Found'),
])
def test_get_method(app, path, expected_response):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.get, path)

    request, response = app.test_client.get(path)

    if path == '/get':
        assert response.text == expected_response
    else:
        assert response.status == 404
        assert "Not Found" in response.text

def test_get_method_with_query(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView.get, '/get_with_query')

    request, response = app.test_client.get('/get_with_query?param=value')

    assert response.text == 'I am get method'
    assert request.query_string == 'param=value'