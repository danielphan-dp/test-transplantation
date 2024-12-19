import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('path, expected_text', [
    ('/', 'I am get method'),
    ('/foo', 'I am get method'),
    ('/bar', 'I am get method'),
])
def test_get_method(app, path, expected_text):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, path)

    request, response = app.test_client.get(path)

    assert response.status == 200
    assert response.text == expected_text

def test_get_method_not_found(app):
    request, response = app.test_client.get('/nonexistent')

    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_params(app):
    class DummyView:
        def get(self, request):
            return text(f'I am get method with query: {request.args}')

    app.add_route(DummyView().get, '/query')

    request, response = app.test_client.get('/query?param=value')

    assert response.status == 200
    assert response.text == 'I am get method with query: MultiDictProxy([("param", "value")])'