import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.post("/test_post")
    def post_method(request):
        return text('I am post method')

    request, response = app.test_client.post("/test_post")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_invalid_route(app):
    request, response = app.test_client.post("/invalid_route")
    assert response.status == 404

def test_post_method_with_data(app):
    @app.post("/test_post_data")
    def post_method_with_data(request):
        return text(request.json)

    request, response = app.test_client.post("/test_post_data", json={"key": "value"})
    assert response.status == 200
    assert response.text == '{"key": "value"}'