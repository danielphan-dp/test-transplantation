import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get")
    def get_method_with_params(request):
        return text(f'I am get method with params: {request.args}')

    request, response = app.test_client.get("/get?param1=value1")
    assert response.text == 'I am get method with params: MultiDict([("param1", ["value1"])])'