import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent")
    assert response.status == 404

def test_get_method_with_query_param(app):
    @app.route("/get_with_param")
    def get_with_param(request):
        param = request.args.get('param', 'default')
        return text(f'Param is {param}')

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.status == 200
    assert response.text == 'Param is test'

def test_get_method_empty_response(app):
    @app.route("/get_empty")
    def get_empty(request):
        return text('')

    request, response = app.test_client.get("/get_empty")
    assert response.status == 200
    assert response.text == ''