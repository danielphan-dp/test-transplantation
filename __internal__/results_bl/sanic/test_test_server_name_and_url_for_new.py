import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_url_for_without_server_name(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    request, response = app.test_client.get("/url-for")
    assert request.url_for("url_for") == "http://localhost:8000/url-for"

def test_url_for_with_server_name(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    app.config.SERVER_NAME = "my-server"
    request, response = app.test_client.get("/url-for")
    assert request.url_for("url_for") == "http://my-server/url-for"

def test_url_for_with_https_server_name(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    app.config.SERVER_NAME = "https://my-server"
    request, response = app.test_client.get("/url-for")
    assert request.url_for("url_for") == "https://my-server/url-for"

def test_url_for_with_path_in_server_name(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    app.config.SERVER_NAME = "https://my-server/path"
    request, response = app.test_client.get("/url-for")
    assert request.url_for("url_for") == "https://my-server/path/url-for"

def test_url_for_with_invalid_route(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    with pytest.raises(Exception):
        app.url_for("non_existent_handler")