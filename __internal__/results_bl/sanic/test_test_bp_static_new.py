import asyncio
import inspect
import os
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app: Sanic):
    @app.route('/get', methods=['GET'])
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get('/get')
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_not_found(app: Sanic):
    request, response = app.test_client.get('/nonexistent')
    assert response.status == 404

def test_get_method_with_query_params(app: Sanic):
    @app.route('/get', methods=['GET'])
    async def get_method(request):
        return text(f'Query params: {request.args}')

    request, response = app.test_client.get('/get?param1=value1&param2=value2')
    assert response.status == 200
    assert response.body == b'Query params: OrderedDict([('param1', ['value1']), ('param2', ['value2'])])'