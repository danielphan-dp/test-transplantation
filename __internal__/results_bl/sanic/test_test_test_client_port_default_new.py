import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.testing import SanicTestClient, PORT

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/get")
    def handler(request):
        return text('I am get method')
    return app

def test_get_method_response(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_status_code(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get")
    assert response.status == 200

def test_get_method_port(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get")
    assert test_client.port > 0

def test_get_method_invalid_route(app):
    test_client = SanicTestClient(app)
    request, response = test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get")
    def handler(request):
        return text(f'Query param: {request.args.get("param")}')
    
    test_client = SanicTestClient(app)
    request, response = test_client.get("/get?param=test")
    assert response.text == 'Query param: test'