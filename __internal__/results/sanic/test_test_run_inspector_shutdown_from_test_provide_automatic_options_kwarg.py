import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def client(app):
    return app.test_client

@app.route("/post", methods=["POST"])
async def post_method(request):
    return text('I am post method')

def test_post_method_success(client):
    request, response = client.post("/post")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_invalid_method(client):
    request, response = client.get("/post")
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text

def test_post_method_with_data(client):
    request, response = client.post("/post", data={"key": "value"})
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_empty_body(client):
    request, response = client.post("/post", data="")
    assert response.status == 200
    assert response.text == "I am post method"