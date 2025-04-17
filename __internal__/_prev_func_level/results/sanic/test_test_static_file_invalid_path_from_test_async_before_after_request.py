import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_with_query_param(app):
    @app.route("/get")
    def get_method_with_param(request):
        param = request.args.get('param', 'default')
        return text(f'I am get method with param: {param}')

    request, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == 'I am get method with param: test'

def test_get_method_no_query_param(app):
    @app.route("/get")
    def get_method_no_param(request):
        return text('I am get method with no param')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method with no param'