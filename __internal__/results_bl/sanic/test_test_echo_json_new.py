import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.post("/post")
    async def post_handler(request):
        return text('I am post method')
    return app

def test_post_method_success(app):
    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_data(app):
    data = {"key": "value"}
    request, response = app.test_client.post("/post", json=data)
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_empty_request(app):
    request, response = app.test_client.post("/post", json={})
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid")
    assert response.status == 404

def test_post_method_no_json(app):
    request, response = app.test_client.post("/post", data="Not JSON")
    assert response.status == 200
    assert response.text == 'I am post method'