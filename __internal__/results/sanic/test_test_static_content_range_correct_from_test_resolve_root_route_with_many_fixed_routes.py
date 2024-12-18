import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_method_response(file_name):
    app = Sanic("test_app")

    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route():
    app = Sanic("test_app")

    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params():
    app = Sanic("test_app")

    @app.get("/test")
    def get_method(request):
        return text(f'I am get method with query param: {request.args.get("param")}')

    request, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == 'I am get method with query param: value'