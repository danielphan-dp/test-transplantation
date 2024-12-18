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
    with pytest.raises(URLBuildError):
        app.url_for("nonexistent")

def test_url_for_with_query_params(app):
    @app.route("/url-for/<param>", name="url_for_with_param")
    async def handler(request, param):
        return text(f"param: {param}")

    assert app.url_for("url_for_with_param", param="test") == "/url-for/test"
    request, response = app.test_client.get("/url-for/test")
    assert response.status == 200
    assert response.text == "param: test"

def test_url_for_with_invalid_param(app):
    @app.route("/url-for/<param:int>", name="url_for_with_int_param")
    async def handler(request, param):
        return text(f"param: {param}")

    with pytest.raises(URLBuildError):
        app.url_for("url_for_with_int_param", param="not_an_int")