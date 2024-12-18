import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

def test_url_for_with_valid_route():
    app = Sanic("app")

    @app.route("/url-for", name="url_for_route")
    def url_for_handler(request):
        return text("url-for")

    assert app.router.routes_all[("url-for",)].name == "app.url_for_route"
    assert app.url_for("url_for_route") == "/url-for"

def test_url_for_with_nonexistent_route():
    app = Sanic("app")

    @app.route("/url-for", name="url_for_route")
    def url_for_handler(request):
        return text("url-for")

    with pytest.raises(URLBuildError):
        app.url_for("nonexistent_route")

def test_url_for_with_query_parameters():
    app = Sanic("app")

    @app.route("/url-for", name="url_for_route")
    def url_for_handler(request):
        return text("url-for")

    assert app.url_for("url_for_route", param1="value1", param2="value2") == "/url-for?param1=value1&param2=value2"

def test_url_for_with_invalid_parameters():
    app = Sanic("app")

    @app.route("/url-for/<param>", name="url_for_route")
    def url_for_handler(request, param):
        return text("url-for")

    with pytest.raises(URLBuildError):
        app.url_for("url_for_route")  # Missing required parameter

def test_url_for_with_different_http_methods():
    app = Sanic("app")

    @app.get("/url-for", name="url_for_get")
    async def url_for_get_handler(request):
        return text("GET url-for")

    @app.post("/url-for", name="url_for_post")
    async def url_for_post_handler(request):
        return text("POST url-for")

    assert app.url_for("url_for_get") == "/url-for"
    assert app.url_for("url_for_post") == "/url-for"