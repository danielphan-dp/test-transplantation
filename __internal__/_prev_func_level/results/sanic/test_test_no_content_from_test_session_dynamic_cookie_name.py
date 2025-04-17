import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("test_app")

    @app.route("/get", methods=["GET"])
    def get(request):
        return text("I am get method")

    return app

def test_get_method(json_app):
    request, response = json_app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"
    assert "Content-Length" in response.headers
    assert response.headers["Content-Length"] == str(len(response.text))
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"

def test_get_method_no_content(json_app):
    request, response = json_app.test_client.get("/no-content")
    assert response.status == 204
    assert response.text == ""
    assert "Content-Length" not in response.headers

def test_get_method_unmodified(json_app):
    request, response = json_app.test_client.get("/unmodified")
    assert response.status == 304
    assert response.text == ""
    assert "Content-Length" not in response.headers
    assert "Content-Type" not in response.headers

def test_get_method_invalid_route(json_app):
    request, response = json_app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_with_query_params(json_app):
    request, response = json_app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"