import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.testing import HOST, PORT

@pytest.mark.parametrize('path, expected_response', [
    ('/', 'I am get method'),
    ('/foo', 'I am get method'),
    ('/bar', 'I am get method'),
])
def test_get_method_responses(app, path, expected_response):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, path)

    request, response = app.test_client.get(path)

    assert response.text == expected_response
    assert response.status == 200

@pytest.mark.parametrize('path', [
    ('/invalid_path'),
])
def test_get_method_invalid_path(app, path):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, path)

    request, response = app.test_client.get(path)

    assert response.status == 404
    assert "Requested URL" in response.text

def test_get_method_with_ssl_context(app):
    context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(localhost_cert, localhost_key)

    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/secure')

    request, response = app.test_client.get(
        f"https://{HOST}:{PORT}/secure",
        server_kwargs={"ssl": context},
    )

    assert response.text == 'I am get method'
    assert response.status == 200