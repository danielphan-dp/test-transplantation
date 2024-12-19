import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')
    return app

def test_url_for_basic(app):
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_forwarded_request(app):
    @app.get("/")
    def handler(request):
        return text("OK")

    @app.get("/another_view/")
    def view_name(request):
        return text("OK")

    app.config.SERVER_NAME = "my-server"
    app.config.PROXIES_COUNT = 1
    request, response = app.test_client.get(
        "/",
        headers={
            "X-Forwarded-For": "127.1.2.3",
            "X-Forwarded-Proto": "https",
            "X-Forwarded-Port": "6789",
        },
    )
    assert app.url_for("view_name") == "/another_view"
    assert (
        app.url_for("view_name", _external=True)
        == "http://my-server/another_view"
    )
    assert (
        request.url_for("view_name") == "https://my-server:6789/another_view"
    )

    request, response = app.test_client.get(
        "/",
        headers={
            "X-Forwarded-For": "127.1.2.3",
            "X-Forwarded-Proto": "https",
            "X-Forwarded-Port": "443",
        },
    )
    assert request.url_for("view_name") == "https://my-server/another_view"

def test_url_for_with_invalid_route(app):
    request, response = app.test_client.get('/nonexistent')
    assert response.status == 404

def test_url_for_with_no_forwarded_headers(app):
    request, response = app.test_client.get("/")
    assert app.url_for("view_name") == "/another_view"
    assert request.url_for("view_name") == "http://localhost/another_view"

def test_url_for_with_different_server_name(app):
    app.config.SERVER_NAME = "another-server"
    request, response = app.test_client.get(
        "/",
        headers={
            "X-Forwarded-For": "127.1.2.3",
            "X-Forwarded-Proto": "http",
            "X-Forwarded-Port": "80",
        },
    )
    assert (
        app.url_for("view_name", _external=True)
        == "http://another-server/another_view"
    )