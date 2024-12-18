import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.post("/post", name="post_route")
    def post_handler(request):
        return text("I am post method")

    return app

def test_post_route(app, sanic_client):
    request, response = sanic_client.post("/post")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_route_name(app):
    assert app.router.routes_all[("post",)].name == "test_app.post_route"
    assert app.url_for("post_route") == "/post"

def test_post_route_invalid_method(app, sanic_client):
    request, response = sanic_client.get("/post")
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text

def test_post_route_url_build_error(app):
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")