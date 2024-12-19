import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_post_method(app):
    @app.post("/post")
    async def post(request):
        return text('I am post method')

    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_data(app):
    @app.post("/post")
    async def post(request):
        return text('I am post method')

    request, response = app.test_client.post("/post", data="Test data")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_empty_body(app):
    @app.post("/post")
    async def post(request):
        return text('I am post method')

    request, response = app.test_client.post("/post", data="")
    assert response.status == 200
    assert response.text == 'I am post method'