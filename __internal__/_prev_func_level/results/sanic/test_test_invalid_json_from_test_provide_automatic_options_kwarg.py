import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.post("/")
    async def handler(request):
        return text('I am post method')

    request, response = app.test_client.post("/")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_invalid_data(app):
    @app.post("/")
    async def handler(request):
        return text('I am post method')

    data = "Invalid data"
    request, response = app.test_client.post("/", data=data)
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_empty_body(app):
    @app.post("/")
    async def handler(request):
        return text('I am post method')

    request, response = app.test_client.post("/", data="")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_headers(app):
    @app.post("/")
    async def handler(request):
        return text('I am post method')

    headers = {"Content-Type": "application/json"}
    request, response = app.test_client.post("/", headers=headers)
    assert response.status == 200
    assert response.text == 'I am post method'