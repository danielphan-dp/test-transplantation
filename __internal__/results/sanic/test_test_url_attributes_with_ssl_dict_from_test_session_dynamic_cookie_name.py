import pytest
from sanic import Sanic
from sanic.response import text

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

@pytest.mark.parametrize('invalid_path', [
    ('/invalid'),
    ('/notfound'),
])
def test_get_method_invalid_paths(app, invalid_path):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/valid')

    request, response = app.test_client.get(invalid_path)
    
    assert response.status == 404
    assert "Requested URL" in response.text

def test_get_method_with_ssl(app):
    ssl_dict = {"cert": localhost_cert, "key": localhost_key}

    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/secure')

    request, response = app.test_client.get(
        'https://localhost:8000/secure',
        server_kwargs={"ssl": ssl_dict},
    )

    assert response.text == 'I am get method'
    assert response.status == 200