import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/get")
    def get_handler(request):
        return text('I am get method')
    return app

def test_get_method_success(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_custom_header(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_server_port(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get", headers={"Host": "my-server"})
    assert request.server_port == 80