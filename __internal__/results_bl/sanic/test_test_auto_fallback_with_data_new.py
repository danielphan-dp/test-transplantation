import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.post("/test")
    def post_method(request):
        return text('I am post method')
    return app

def test_post_method_success(app):
    _, response = app.test_client.post("/test")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.text == 'I am post method'

def test_post_method_with_data(app):
    _, response = app.test_client.post("/test", json={"key": "value"})
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.text == 'I am post method'

def test_post_method_with_empty_data(app):
    _, response = app.test_client.post("/test", json={})
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.text == 'I am post method'

def test_post_method_with_invalid_route(app):
    _, response = app.test_client.post("/invalid")
    assert response.status == 404
    assert response.content_type == "text/plain; charset=utf-8"