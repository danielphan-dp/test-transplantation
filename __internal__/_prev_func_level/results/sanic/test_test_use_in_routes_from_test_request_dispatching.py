import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.route("/", methods=["POST"])
    def handler(request):
        return text("I am post method")

    request, response = app.test_client.post("/")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_with_invalid_route(app):
    request, response = app.test_client.get("/")
    assert response.status == 405
    assert "Method GET not allowed for URL /" in response.text

def test_post_method_with_data(app):
    @app.route("/data", methods=["POST"])
    def data_handler(request):
        return text(request.json.get("key", "default"))

    request, response = app.test_client.post("/data", json={"key": "value"})
    assert response.status == 200
    assert response.text == "value"

def test_post_method_with_empty_data(app):
    @app.route("/data", methods=["POST"])
    def data_handler(request):
        return text(request.json.get("key", "default"))

    request, response = app.test_client.post("/data", json={})
    assert response.status == 200
    assert response.text == "default"