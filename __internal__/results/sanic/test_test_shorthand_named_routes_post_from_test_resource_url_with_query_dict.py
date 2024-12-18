import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

def test_url_for_with_valid_route():
    app = Sanic("app")

    @app.route("/url-for", name="url_for_route")
    def url_for_handler(request):
        return text("url-for")

    assert app.router.routes_all[("GET", "/url-for")].name == "app.url_for_route"
    assert app.url_for("url_for_route") == "/url-for"

def test_url_for_with_invalid_route():
    app = Sanic("app")

    @app.route("/url-for", name="url_for_route")
    def url_for_handler(request):
        return text("url-for")

    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")

def test_url_for_with_query_parameters():
    app = Sanic("app")

    @app.route("/url-for", name="url_for_route")
    def url_for_handler(request):
        return text("url-for")

    assert app.url_for("url_for_route", param1="value1") == "/url-for?param1=value1"

def test_url_for_with_multiple_query_parameters():
    app = Sanic("app")

    @app.route("/url-for", name="url_for_route")
    def url_for_handler(request):
        return text("url-for")

    assert app.url_for("url_for_route", param1="value1", param2="value2") == "/url-for?param1=value1&param2=value2"

def test_url_for_with_no_route_name():
    app = Sanic("app")

    @app.route("/url-for", name="url_for_route")
    def url_for_handler(request):
        return text("url-for")

    with pytest.raises(URLBuildError):
        app.url_for("")