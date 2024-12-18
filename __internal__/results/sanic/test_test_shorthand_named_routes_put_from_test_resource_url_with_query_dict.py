import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

def test_url_for_with_valid_route():
    app = Sanic("app")

    @app.route("/url-for", name="url_for")
    def url_for(request):
        return text('url-for')

    assert app.router.routes_all[("GET", "/url-for")].name == "app.url_for"
    assert app.url_for("url_for") == "/url-for"

def test_url_for_with_invalid_route():
    app = Sanic("app")

    @app.route("/url-for", name="url_for")
    def url_for(request):
        return text('url-for')

    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")

def test_url_for_with_query_parameters():
    app = Sanic("app")

    @app.route("/url-for", name="url_for")
    def url_for(request):
        return text('url-for')

    assert app.url_for("url_for", param1="value1", param2="value2") == "/url-for?param1=value1&param2=value2"

def test_url_for_with_different_http_methods():
    app = Sanic("app")

    @app.route("/url-for", methods=["POST"], name="url_for_post")
    def url_for_post(request):
        return text('url-for post')

    assert app.router.routes_all[("POST", "/url-for")].name == "app.url_for_post"
    assert app.url_for("url_for_post") == "/url-for"

def test_url_for_with_slash_suffix():
    app = Sanic("app")

    @app.route("/url-for/", name="url_for_slash")
    def url_for_slash(request):
        return text('url-for with slash')

    assert app.router.routes_all[("GET", "/url-for/")].name == "app.url_for_slash"
    assert app.url_for("url_for_slash") == "/url-for/"