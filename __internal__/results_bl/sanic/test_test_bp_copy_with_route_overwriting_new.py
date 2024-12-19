import pytest
from sanic import Sanic, Blueprint
from sanic.response import text
from sanic.exceptions import NotFound

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get")
    async def get_method(request):
        return text(f'I am get method with param: {request.args.get("param", "none")}')

    _, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == 'I am get method with param: test'