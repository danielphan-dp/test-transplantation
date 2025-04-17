import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_request_cookies_with_cookies(app):
    request, response = app.test_client.get("/", cookies={"type": "test"})
    assert request.cookies.get('type') == "test"

def test_request_headers(app):
    request, response = app.test_client.get("/", headers={"X-Foo": "bar"})
    assert request.headers.get('X-Foo') == "bar"

def test_request_path(app):
    request, response = app.test_client.get("/")
    assert request.path == "/"

def test_request_method(app):
    request, response = app.test_client.get("/")
    assert request.method == "GET"

def test_request_content_length(app):
    request, response = app.test_client.get("/")
    assert request.content_length == 0

def test_request_params(app):
    request, response = app.test_client.get("/?foo=bar")
    assert request.params.get('foo') == "bar"
    assert request.GET.get('foo') == "bar"