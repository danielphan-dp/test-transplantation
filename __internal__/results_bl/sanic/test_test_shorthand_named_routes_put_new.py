import asyncio
import pytest
from sanic import Sanic
from sanic.exceptions import URLBuildError
from sanic.response import text

def test_url_for_route(app):
    @app.route('/url-for', name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    assert app.router.routes_all[("GET", "/url-for")].name == "app.url_for_route"
    assert app.url_for("url_for_route") == "/url-for"

def test_url_for_non_existent_route(app):
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")

def test_url_for_with_different_method(app):
    @app.put("/put", name="route_put")
    def handler(request):
        return text("OK")

    assert app.url_for("route_put") == "/put"
    with pytest.raises(URLBuildError):
        app.url_for("url_for_route")  # Testing URL for a different method

def test_url_for_with_query_parameters(app):
    @app.route('/url-for', methods=['GET'], name='url_for_route_with_query')
    def url_for_handler_with_query(request):
        return text('url-for with query')

    assert app.url_for("url_for_route_with_query", param1='value1') == "/url-for?param1=value1"