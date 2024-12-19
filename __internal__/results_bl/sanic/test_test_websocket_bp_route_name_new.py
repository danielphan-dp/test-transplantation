import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.testing import SanicTestClient
from sanic.blueprints import Blueprint

app = Sanic("test_app")

@app.route('/url-for')
def url_for(request):
    return text('url-for')

@pytest.mark.parametrize('name,expected', (
    ('test_route', '/bp/route'),
    ('test_route2', '/bp/route2'),
    ('foobar_3', '/bp/route3'),
    ('non_existent_route', None),  # Edge case for non-existent route
))
def test_url_for_route_name(app, name, expected):
    """Tests that url_for returns the correct route or None for non-existent routes."""
    event = asyncio.Event()
    bp = Blueprint("test_bp", url_prefix="/bp")

    @bp.get("/main")
    async def main(request): 
        return text('main')

    @bp.websocket("/route")
    async def test_route(request, ws):
        event.set()

    @bp.websocket("/route2")
    async def test_route2(request, ws):
        event.set()

    @bp.websocket("/route3", name="foobar_3")
    async def test_route3(request, ws):
        event.set()

    app.blueprint(bp)

    uri = app.url_for("test_bp.main")
    assert uri == "/bp/main"

    if expected:
        uri = app.url_for(f"test_bp.{name}")
        assert uri == expected
        request, response = SanicTestClient(app).websocket(uri)
        assert response.opened is True
        assert event.is_set()
    else:
        with pytest.raises(Exception):
            app.url_for(f"test_bp.{name}")  # Expecting an exception for non-existent route