import pytest
from sanic import Sanic
from sanic.exceptions import URLBuildError
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/url-for", name="url_for")
    def url_for(request):
        return text('url-for')

    return app

def test_url_for_existing_route(app):
    assert app.url_for("url_for") == "/url-for"

def test_url_for_non_existent_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_route")
        e.match("Endpoint with name `test_app.non_existent_route` was not found")

def test_url_for_with_params(app):
    @app.route("/user/<id:int>", methods=["GET"], name="user_profile")
    def user_profile(request, id):
        return text(f"User {id}")

    assert app.url_for("user_profile", id=42) == "/user/42"

def test_url_for_with_invalid_params(app):
    @app.route("/item/<item_id:int>", methods=["GET"], name="item_detail")
    def item_detail(request, item_id):
        return text(f"Item {item_id}")

    with pytest.raises(URLBuildError) as e:
        app.url_for("item_detail")  # Missing required parameter
        e.match("Required parameter `item_id` was not passed to url_for")