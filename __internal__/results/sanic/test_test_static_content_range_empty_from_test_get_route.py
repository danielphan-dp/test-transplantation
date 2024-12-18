import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path', ['/nonexistent', '/another_invalid_path'])
def test_get_invalid_routes(request_path):
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 404
    assert "Requested URL" in response.text

def test_get_method_response():
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'