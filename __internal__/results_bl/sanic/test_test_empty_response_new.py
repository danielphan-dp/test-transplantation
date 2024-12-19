import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.get("/get_test")
def get_handler(request):
    return text('I am get method')

def test_get_method_response(app):
    request, response = app.test_client.get("/get_test")
    assert response.content_type == 'text/plain; charset=utf-8'
    assert response.body == b'I am get method'

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get_test", headers={})
    assert response.content_type == 'text/plain; charset=utf-8'
    assert response.body == b'I am get method'

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get_test?param=value")
    assert response.content_type == 'text/plain; charset=utf-8'
    assert response.body == b'I am get method'