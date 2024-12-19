import asyncio
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get")
    def get_method_with_params(request):
        return text(f'I am get method with params: {request.args}')

    request, response = app.test_client.get("/get?param1=value1&param2=value2")
    assert response.text == 'I am get method with params: MultiDict([(\'param1\', [\'value1\']), (\'param2\', [\'value2\'])])'