import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

class TestPostMethod(HTTPMethodView):
    def post(self, request):
        return text('I am post method')

@pytest.fixture
def app():
    app = Sanic("TestApp")
    app.add_route(TestPostMethod.as_view(), "/post_method")
    return app

def test_post_method_success(app):
    request, response = app.test_client.post("/post_method")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_data(app):
    data = "Test data"
    request, response = app.test_client.post("/post_method", data=data)
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_empty_request(app):
    request, response = app.test_client.post("/post_method", data="")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid_route")
    assert response.status == 404

def test_post_method_with_large_data(app):
    data = "A" * 10000
    request, response = app.test_client.post("/post_method", data=data)
    assert response.status == 200
    assert response.text == 'I am post method'