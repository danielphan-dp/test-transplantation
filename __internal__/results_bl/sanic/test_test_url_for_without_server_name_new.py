import pytest
from sanic import Sanic
from sanic.response import text, json

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/url-for")
    def url_for(request):
        return text("url-for")

    return app

def test_url_for_with_invalid_request(app):
    request, response = app.test_client.get("/url-for?invalid_param=1")
    assert response.status == 200
    assert response.text == "url-for"

def test_url_for_with_different_http_methods(app):
    request, response = app.test_client.post("/url-for")
    assert response.status == 405  # Method Not Allowed

def test_url_for_with_custom_header(app):
    request, response = app.test_client.get("/url-for", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "url-for"

def test_url_for_without_server_name(app):
    @app.route("/sample")
    def sample(request):
        return json({"url": request.url_for("url_for")})

    request, response = app.test_client.get("/sample")
    assert response.json["url"] == f"http://127.0.0.1:{request.server_port}/url-for"