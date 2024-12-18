import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method(json_app):
    request, response = json_app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"
    assert "Content-Length" in response.headers
    assert response.headers["Content-Length"] == str(len(response.text))
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"

def test_get_method_with_invalid_route(json_app):
    request, response = json_app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(json_app):
    request, response = json_app.test_client.get("/", headers={"Custom-Header": "Test"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers["Custom-Header"] != "Test"  # Ensure custom header is not present in response

def test_get_method_empty_response(json_app):
    @json_app.get("/empty")
    def empty_response(request):
        return text("", status=204)

    request, response = json_app.test_client.get("/empty")
    assert response.status == 204
    assert response.text == ""
    assert "Content-Length" not in response.headers

def test_get_method_unmodified_response(json_app):
    @json_app.get("/unmodified")
    def unmodified_response(request):
        return text("", status=304)

    request, response = json_app.test_client.get("/unmodified")
    assert response.status == 304
    assert response.text == ""
    assert "Content-Length" not in response.headers
    assert "Content-Type" not in response.headers