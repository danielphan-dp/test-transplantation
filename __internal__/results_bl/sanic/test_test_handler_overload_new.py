import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.post("/test/post")
    def post_handler(request):
        return text('I am post method')

    _, response = app.test_client.post("/test/post")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_data(app):
    @app.post("/test/post/data")
    def post_handler_with_data(request):
        return text(request.json)

    _, response = app.test_client.post("/test/post/data", json={"key": "value"})
    assert response.status == 200
    assert response.text == '{"key": "value"}'

def test_post_method_empty_body(app):
    @app.post("/test/post/empty")
    def post_handler_empty(request):
        return text('Empty body received')

    _, response = app.test_client.post("/test/post/empty", json={})
    assert response.status == 200
    assert response.text == 'Empty body received'

def test_post_method_invalid_route(app):
    @app.post("/test/post/invalid")
    def post_handler_invalid(request):
        return text('Invalid route')

    _, response = app.test_client.post("/test/post/nonexistent")
    assert response.status == 404