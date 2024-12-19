import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import SanicException

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    @app.get("/api/v1/test/")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get('/api/v1/test/')
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    @app.get("/api/v1/test/")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get('/api/v1/nonexistent/')
    assert response.status == 404

def test_get_method_invalid_route(app):
    @app.get("/api/v1/<user>/<user>/")
    def handler(request, user):
        return text("OK")

    with pytest.raises(SanicException):
        app.router.finalize()