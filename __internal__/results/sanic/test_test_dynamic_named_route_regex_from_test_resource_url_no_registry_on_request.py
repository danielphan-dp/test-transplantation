import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_basic(app):
    @app.route("/url-for", name="url_for")
    async def handler(request):
        return text("url-for")

    assert app.url_for("url_for") == "/url-for"
    request, response = app.test_client.get("/url-for")
    assert response.status == 200
    assert response.text == "url-for"

def test_url_for_with_nonexistent_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("nonexistent")
        assert str(e.value) == "Endpoint with name `app.nonexistent` was not found"

def test_url_for_with_params(app):
    @app.route("/user/<user_id:int>", name="user_profile")
    async def user_profile(request, user_id):
        return text(f"User ID: {user_id}")

    assert app.url_for("user_profile", user_id=42) == "/user/42"
    request, response = app.test_client.get("/user/42")
    assert response.status == 200
    assert response.text == "User ID: 42"

def test_url_for_with_invalid_params(app):
    @app.route("/item/<item_id:int>", name="item_detail")
    async def item_detail(request, item_id):
        return text(f"Item ID: {item_id}")

    with pytest.raises(URLBuildError) as e:
        app.url_for("item_detail")  # Missing required parameter
        assert str(e.value) == "Required parameter `item_id` was not passed to url_for"