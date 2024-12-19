import asyncio
import pytest
from sanic import Sanic
from sanic.exceptions import URLBuildError
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("app")
    return app

def test_url_for_valid_route(app):
    @app.route('/url-for', name='url_for_route')
    def url_for(request):
        return text('url-for')

    assert app.url_for('url_for_route') == '/url-for'

def test_url_for_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_without_name(app):
    @app.route('/no-name')
    def no_name_route(request):
        return text('no-name')

    assert app.url_for('no-name') == '/no-name'  # This should raise an error since the route has no name

def test_url_for_multiple_routes(app):
    @app.route('/first', name='first_route')
    def first_route(request):
        return text('first')

    @app.route('/second', name='second_route')
    def second_route(request):
        return text('second')

    assert app.url_for('first_route') == '/first'
    assert app.url_for('second_route') == '/second'