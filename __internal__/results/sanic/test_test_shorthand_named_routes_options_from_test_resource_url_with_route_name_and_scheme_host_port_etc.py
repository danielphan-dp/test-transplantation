import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

def test_url_for_with_valid_route_name():
    app = Sanic("app")

    @app.route("/url-for", name="url_for_route")
    def url_for_handler(request):
        return text("url-for")

    assert app.router.routes_all[("url-for",)].name == "app.url_for_route"
    assert app.url_for("url_for_route") == "/url-for"

def test_url_for_with_invalid_route_name():
    app = Sanic("app")

    @app.route("/url-for", name="url_for_route")
    def url_for_handler(request):
        return text("url-for")

    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")

def test_url_for_with_additional_params():
    app = Sanic("app")

    @app.route("/url-for/<param>", name="url_for_with_param")
    def url_for_param_handler(request, param):
        return text(f"url-for with param: {param}")

    assert app.url_for("url_for_with_param", param="test") == "/url-for/test"

def test_url_for_with_missing_param():
    app = Sanic("app")

    @app.route("/url-for/<param>", name="url_for_with_param")
    def url_for_param_handler(request, param):
        return text(f"url-for with param: {param}")

    with pytest.raises(URLBuildError):
        app.url_for("url_for_with_param")