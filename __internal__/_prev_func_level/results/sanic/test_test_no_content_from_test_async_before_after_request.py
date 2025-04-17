import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(json_app):
    request, response = json_app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"
    assert "Content-Length" in response.headers
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"

def test_get_method_invalid_route(json_app):
    request, response = json_app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param(json_app):
    request, response = json_app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_no_content(json_app):
    request, response = json_app.test_client.get("/get", headers={"If-None-Match": "some-etag"})
    assert response.status == 304
    assert response.text == ""
    assert "Content-Length" not in response.headers
    assert "Content-Type" not in response.headers