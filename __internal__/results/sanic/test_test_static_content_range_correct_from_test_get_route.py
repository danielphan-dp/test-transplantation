import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_method_response(file_name, static_file_directory):
    app = Sanic("test_app")

    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_method_with_invalid_route(file_name, static_file_directory):
    app = Sanic("test_app")

    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_method_with_query_params(file_name, static_file_directory):
    app = Sanic("test_app")

    @app.get("/test")
    def get_method(request):
        param = request.args.get('param', 'default')
        return text(f'I am get method with param: {param}')

    request, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == 'I am get method with param: value'

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method with param: default'