import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.post("/post")
    async def handler(request):
        return text("I am post method")

    request, response = app.test_client.post("/post")
    assert response.text == "I am post method"

    request, response = app.test_client.get("/post")
    assert response.status == 405

def test_post_with_data(app):
    @app.post("/post")
    async def handler(request):
        return text("Received data: " + request.json.get("data", ""))

    request, response = app.test_client.post("/post", json={"data": "test"})
    assert response.text == "Received data: test"

def test_post_empty_body(app):
    @app.post("/post")
    async def handler(request):
        return text("Body is empty" if not request.body else "Body received")

    request, response = app.test_client.post("/post", data="")
    assert response.text == "Body is empty"

def test_post_invalid_method(app):
    @app.post("/post")
    async def handler(request):
        return text("I am post method")

    request, response = app.test_client.put("/post")
    assert response.status == 405

def test_post_with_headers(app):
    @app.post("/post")
    async def handler(request):
        return text("Headers received: " + str(request.headers))

    headers = {"Custom-Header": "Value"}
    request, response = app.test_client.post("/post", headers=headers)
    assert "Custom-Header" in response.text
    assert "Value" in response.text