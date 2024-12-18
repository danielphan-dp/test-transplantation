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

@pytest.mark.parametrize('path', [
    ('/invalid_path'),
])
def test_get_method_not_found(app, path):
    request, response = app.test_client.get(path)
    assert response.status == 404
    assert "Requested URL" in response.text

@pytest.mark.parametrize('path', [
    ('/foo'),
    ('/bar'),
])
def test_get_method_with_query(app, path):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, path)

    request, response = app.test_client.get(path + '?query=1')
    assert response.status == 200
    assert response.text == 'I am get method'