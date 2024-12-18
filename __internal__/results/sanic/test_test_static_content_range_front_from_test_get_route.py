import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_method(file_name):
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method with query')

    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == 'I am get method with query'