import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

def test_url_for_with_valid_route():
    app = Sanic("app")

    @app.route("/url-for", name="url_for")
    def url_for_handler(request):
        return text("url-for")

    assert app.router.routes_all[("url-for",)].name == "app.url_for"
    assert app.url_for("url_for") == "/url-for"

def test_url_for_with_nonexistent_route():
    app = Sanic("app")

    with pytest.raises(URLBuildError) as e:
        app.url_for("nonexistent_route")
        e.match("Endpoint with name `app.nonexistent_route` was not found")

def test_url_for_with_parameters():
    app = Sanic("app")

    @app.route("/user/<id:int>", name="user_profile")
    def user_profile(request, id):
        return text(f"User ID: {id}")

    assert app.url_for("user_profile", id=42) == "/user/42"

def test_url_for_with_missing_parameters():
    app = Sanic("app")

    @app.route("/user/<id:int>", name="user_profile")
    def user_profile(request, id):
        return text(f"User ID: {id}")

    with pytest.raises(URLBuildError) as e:
        app.url_for("user_profile")
        e.match("Required parameter `id` was not passed to url_for")