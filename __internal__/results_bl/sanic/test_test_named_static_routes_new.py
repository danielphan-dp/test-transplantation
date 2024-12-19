import asyncio
import pytest
from sanic import Sanic
from sanic.exceptions import URLBuildError
from sanic.response import text

def test_url_for():
    app = Sanic("app")

    @app.route('/url-for', name='url_for_route')
    async def url_for_handler(request):
        return text('url-for')

    assert app.router.routes_all[('/url-for',)].name == 'app.url_for_route'
    assert app.url_for('url_for_route') == '/url-for'
    
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

    @app.route('/another-route', name='another_route')
    async def another_handler(request):
        return text('another route')

    assert app.router.routes_all[('/another-route',)].name == 'app.another_route'
    assert app.url_for('another_route') == '/another-route'
    
    with pytest.raises(URLBuildError):
        app.url_for('url_for_route', extra_arg='unexpected')