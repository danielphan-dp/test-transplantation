import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method_response(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_data(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method with data")

    payload = "key1=value1&key2=value2"
    headers = {"content-type": "application/x-www-form-urlencoded"}

    request, response = app.test_client.post("/post", data=payload, headers=headers)
    assert response.status == 200
    assert response.text == "I am post method with data"

def test_post_method_empty_payload(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method with empty payload")

    request, response = app.test_client.post("/post", data="")
    assert response.status == 200
    assert response.text == "I am post method with empty payload"

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_post_method_method_not_allowed(app):
    @app.route("/post", methods=["GET"])
    async def handler(request):
        return text("GET method not allowed")

    request, response = app.test_client.post("/post")
    assert response.status == 405
    assert "Method POST not allowed for URL /post" in response.text