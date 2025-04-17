import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

def test_url_for_with_valid_route():
    app = Sanic("app")

    @app.route("/url-for", name="url_for")
    def handler(request):
        return text("url-for")

    assert app.router.routes_all[("url-for",)].name == "app.url_for"
    assert app.url_for("url_for") == "/url-for"
    request, response = app.test_client.get("/url-for")
    assert response.status == 200
    assert response.text == "url-for"

def test_url_for_with_nonexistent_route():
    app = Sanic("app")

    with pytest.raises(URLBuildError):
        app.url_for("nonexistent_route")

def test_url_for_with_query_parameters():
    app = Sanic("app")

    @app.route("/url-for", name="url_for_with_query")
    def handler(request):
        return text("url-for with query")

    assert app.url_for("url_for_with_query", param1="value1") == "/url-for?param1=value1"
    request, response = app.test_client.get(app.url_for("url_for_with_query", param1="value1"))
    assert response.status == 200
    assert response.text == "url-for with query"