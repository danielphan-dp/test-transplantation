import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.put("/put", name="route_put")
    def handler(request):
        return text("I am put method")

    return app

def test_put_route(app):
    app_client = app.test_client()
    
    resp = app_client.put("/put")
    assert resp.status == 200
    assert resp.text == "I am put method"

def test_put_route_name(app):
    assert app.router.routes_all[("put",)].name == "app.route_put"
    assert app.url_for("route_put") == "/put"

def test_invalid_route_name(app):
    with pytest.raises(URLBuildError):
        app.url_for("invalid_handler")