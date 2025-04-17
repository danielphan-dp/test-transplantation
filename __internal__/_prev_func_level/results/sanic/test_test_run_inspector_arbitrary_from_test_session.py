import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("TestApp")

@app.route("/post", methods=["POST"])
def post(request):
    return text('I am post method')

@pytest.fixture
def client():
    return app.test_client

def test_post_method(client):
    request, response = client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_with_data(client):
    request, response = client.post("/post", json={"key": "value"})
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_empty_body(client):
    request, response = client.post("/post", data={})
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_invalid_route(client):
    request, response = client.post("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_post_method_with_headers(client):
    headers = {"Custom-Header": "value"}
    request, response = client.post("/post", headers=headers)
    assert response.status == 200
    assert response.text == 'I am post method'