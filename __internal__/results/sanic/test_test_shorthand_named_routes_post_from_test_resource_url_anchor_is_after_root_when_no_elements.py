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

def test_url_for_with_nonexistent_route():
    app = Sanic("app")

    @app.route("/url-for", name="url_for_route")
    def url_for_handler(request):
        return text("url-for")

    with pytest.raises(URLBuildError):
        app.url_for("nonexistent_route")

def test_url_for_with_parameters():
    app = Sanic("app")

    @app.route("/user/<id:int>", name="user_route")
    def user_handler(request, id):
        return text(f"User ID: {id}")

    assert app.url_for("user_route", id=42) == "/user/42"

def test_url_for_with_missing_parameters():
    app = Sanic("app")

    @app.route("/user/<id:int>", name="user_route")
    def user_handler(request, id):
        return text(f"User ID: {id}")

    with pytest.raises(URLBuildError):
        app.url_for("user_route")