import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/url-for")
    def url_for(request):
        return text('url-for')

    return app

def test_url_for_valid_endpoint(app):
    url = app.url_for("url-for")
    assert url == "/url-for"

def test_url_for_invalid_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_endpoint")
        e.match("Endpoint with name `app.non_existent_endpoint` was not found")

def test_url_for_with_query_params(app):
    @app.route("/query")
    def query_handler(request):
        return text("query response")

    url = app.url_for("query_handler", param1="value1", param2="value2")
    assert url == "/query?param1=value1&param2=value2"

def test_url_for_with_path_params(app):
    @app.route("/path/<param>")
    def path_handler(request, param):
        return text(f"Path param: {param}")

    url = app.url_for("path_handler", param="test")
    assert url == "/path/test"

def test_url_for_with_missing_params(app):
    @app.route("/path/<param>")
    def path_handler(request, param):
        return text(f"Path param: {param}")

    with pytest.raises(URLBuildError) as e:
        app.url_for("path_handler")
        e.match("Required parameter `param` was not passed to url_for")