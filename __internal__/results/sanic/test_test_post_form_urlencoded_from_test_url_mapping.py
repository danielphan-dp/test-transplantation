import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    request, response = app.test_client.post("/post")
    
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_with_data(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text(request.form.get("test", "No data"))

    payload = "test=Hello"
    headers = {"content-type": "application/x-www-form-urlencoded"}

    request, response = app.test_client.post("/post", data=payload, headers=headers)

    assert response.status == 200
    assert response.text == "Hello"

def test_post_empty_data(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text(request.form.get("test", "No data"))

    payload = ""
    headers = {"content-type": "application/x-www-form-urlencoded"}

    request, response = app.test_client.post("/post", data=payload, headers=headers)

    assert response.status == 200
    assert response.text == "No data"

def test_post_invalid_method(app):
    @app.route("/post", methods=["POST"])
    async def handler(request):
        return text("I am post method")

    request, response = app.test_client.get("/post")

    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text