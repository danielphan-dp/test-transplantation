import asyncio
import pytest
from sanic import Sanic
from sanic.exceptions import URLBuildError
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("app")
    return app

@app.route('/url-for')
def url_for(request):
    return text('url-for')

def test_url_for(app):
    @app.route("/folder/<name>", name="route_dynamic")
    async def handler(request, name):
        return text("OK")

    assert app.url_for("route_dynamic", name="test") == "/folder/test"
    assert app.url_for("route_dynamic", name="example") == "/folder/example"

    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")

    @app.route("/static/<path:path>", name="static_route")
    async def static_handler(request, path):
        return text("Static file")

    assert app.url_for("static_route", path="file.txt") == "/static/file.txt"
    assert app.url_for("static_route", path="images/logo.png") == "/static/images/logo.png"

    with pytest.raises(URLBuildError):
        app.url_for("static_handler")