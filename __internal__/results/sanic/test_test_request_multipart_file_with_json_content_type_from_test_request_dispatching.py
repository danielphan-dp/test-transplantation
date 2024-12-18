import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/", methods=["POST"])
    async def post(request):
        return text("I am post method")

    return app

def test_post_method_response(app):
    request, response = app.test_client.post("/")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_invalid_method(app):
    request, response = app.test_client.get("/")
    assert response.status == 405
    assert "Method GET not allowed for URL /" in response.text

def test_post_method_with_empty_body(app):
    request, response = app.test_client.post("/", data="")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_json_content_type(app):
    headers = {"content-type": "application/json"}
    request, response = app.test_client.post("/", data='{"key": "value"}', headers=headers)
    assert response.status == 200
    assert response.text == "I am post method"