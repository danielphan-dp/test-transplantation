import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.post("/")
async def handler(request):
    return text('I am post method')

def test_post_method_valid(app):
    request, response = app.test_client.post("/")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_invalid_data(app):
    data = "I am not json"
    request, response = app.test_client.post("/", data=data)
    assert response.status == 400

def test_post_method_empty_body(app):
    request, response = app.test_client.post("/")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_large_payload(app):
    large_data = 'a' * 10000
    request, response = app.test_client.post("/", data=large_data)
    assert response.status == 200
    assert response.text == 'I am post method'