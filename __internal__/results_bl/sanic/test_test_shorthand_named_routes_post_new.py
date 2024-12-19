import asyncio
import pytest
from sanic import Sanic
from sanic.exceptions import URLBuildError
from sanic.response import text

def test_url_for():
    app = Sanic("app")

    @app.route('/url-for', methods=['GET'], name='url_for_name')
    def url_for_handler(request):
        return text('url-for')

    @app.post("/post", name="route_name")
    def post_handler(request):
        return text("OK")

    assert app.router.routes_all[("get", "/url-for")].name == "app.url_for_name"
    assert app.url_for("url_for_name") == "/url-for"
    assert app.url_for("route_name") == "/post"
    
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")

    with pytest.raises(URLBuildError):
        app.url_for("handler")