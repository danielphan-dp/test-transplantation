import asyncio
import pytest
from sanic import Sanic
from sanic.exceptions import URLBuildError
from sanic.response import text

app = Sanic("app")

@app.route('/url-for')
def url_for(request):
    return text('url-for')

def test_url_for_valid_route():
    url = app.url_for('url_for')
    assert url == '/url-for'

def test_url_for_invalid_route():
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_dynamic_route():
    async def handler(request, unhashable):
        return text("OK")

    app.add_route(
        handler,
        "/folder/<unhashable:[A-Za-z0-9/]+>/end/",
        name="route_unhashable",
    )
    url = app.url_for("route_unhashable", unhashable="folder1")
    assert url == "/folder/folder1/end"

def test_url_for_with_special_characters():
    async def handler(request, unhashable):
        return text("OK")

    app.add_route(
        handler,
        "/folder/<unhashable:[A-Za-z0-9/]+>/end/",
        name="route_unhashable",
    )
    url = app.url_for("route_unhashable", unhashable="folder/with/special")
    assert url == "/folder/folder/with/special/end"

def test_url_for_with_empty_parameter():
    async def handler(request, unhashable):
        return text("OK")

    app.add_route(
        handler,
        "/folder/<unhashable:[A-Za-z0-9/]+>/end/",
        name="route_unhashable",
    )
    with pytest.raises(URLBuildError):
        app.url_for("route_unhashable", unhashable="")