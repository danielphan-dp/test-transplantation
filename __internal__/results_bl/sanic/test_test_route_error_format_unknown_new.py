import logging
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_success(app):
    @app.get("/test")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get('/test')
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    @app.get("/invalid")
    def handler(request):
        return text('This route should not be reached')

    request, response = app.test_client.get('/nonexistent')
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/test")
    def handler(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get('/test?param=value')
    assert response.status == 200
    assert response.text == 'Query param: value'

def test_get_method_error_format(app):
    with pytest.raises(SanicException, match="Unknown format: bad"):
        @app.get("/text", error_format="bad")
        def handler(request):
            return text('This should raise an error')