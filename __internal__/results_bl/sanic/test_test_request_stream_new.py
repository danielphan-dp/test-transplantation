import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_post_method(app):
    @app.post("/post_method")
    def post_method(request):
        return text('I am post method')

    request, response = app.test_client.post("/post_method")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_data(app):
    @app.post("/post_method_with_data")
    def post_method_with_data(request):
        return text(request.json.get('data', ''))

    request, response = app.test_client.post("/post_method_with_data", json={'data': 'test data'})
    assert response.status == 200
    assert response.text == 'test data'

def test_post_method_empty_body(app):
    @app.post("/post_method_empty")
    def post_method_empty(request):
        return text('Empty body received')

    request, response = app.test_client.post("/post_method_empty", data='')
    assert response.status == 200
    assert response.text == 'Empty body received'

def test_post_method_invalid_data(app):
    @app.post("/post_method_invalid")
    def post_method_invalid(request):
        return text('Invalid data received')

    request, response = app.test_client.post("/post_method_invalid", data='invalid data')
    assert response.status == 200
    assert response.text == 'Invalid data received'