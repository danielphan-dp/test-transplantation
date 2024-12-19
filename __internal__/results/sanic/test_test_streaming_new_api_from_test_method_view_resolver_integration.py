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

def test_post_method(app):
    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_with_data(app):
    request, response = app.test_client.post("/post", data="sample data")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_with_empty_data(app):
    request, response = app.test_client.post("/post", data="")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_with_invalid_route(app):
    request, response = app.test_client.post("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_post_with_method_not_allowed(app):
    request, response = app.test_client.get("/post")
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text