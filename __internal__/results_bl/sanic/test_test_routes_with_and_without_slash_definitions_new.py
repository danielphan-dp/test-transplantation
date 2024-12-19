import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method_without_slash(app):
    @app.post("/test")
    def post_method(request):
        return text('I am post method')

    _, response = app.test_client.post("/test")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_slash(app):
    @app.post("/test/")
    def post_method(request):
        return text('I am post method')

    _, response = app.test_client.post("/test/")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_invalid_route(app):
    @app.post("/valid")
    def post_method(request):
        return text('I am post method')

    _, response = app.test_client.post("/invalid")
    assert response.status == 404

def test_post_method_empty_body(app):
    @app.post("/empty")
    def post_method(request):
        return text('I am post method')

    _, response = app.test_client.post("/empty", json={})
    assert response.status == 200
    assert response.text == 'I am post method'