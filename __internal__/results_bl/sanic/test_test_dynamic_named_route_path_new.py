import asyncio
import pytest
from sanic import Sanic
from sanic.exceptions import URLBuildError
from sanic.response import text

def test_url_for():
    app = Sanic("app")

    @app.route('/url-for')
    async def url_for_handler(request):
        return text('url-for')

    route = app.router.routes_all[('/url-for', 'GET')]
    assert route.name == 'app.url_for_handler'
    assert app.url_for('url_for_handler') == '/url-for'

    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

    assert app.url_for('url_for_handler', request=None) == '/url-for'  # Testing with None request
    assert app.url_for('url_for_handler', path='') == '/url-for'  # Testing with empty path
    assert app.url_for('url_for_handler', path='some/path') == '/url-for'  # Testing with irrelevant path argument