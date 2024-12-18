import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    return app

def test_url_for_existing_route(app):
    assert app.url_for('url_for') == '/url-for'

def test_url_for_non_existent_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_query_params(app):
    @app.route('/query')
    def query_handler(request):
        return text('query response')

    assert app.url_for('query_handler') == '/query'
    assert app.url_for('query_handler', param='value') == '/query?param=value'

def test_url_for_with_multiple_routes(app):
    @app.route('/first', name='first_route')
    async def first_handler(request):
        return text('first')

    @app.route('/second', name='second_route')
    async def second_handler(request):
        return text('second')

    assert app.url_for('first_route') == '/first'
    assert app.url_for('second_route') == '/second'

def test_url_for_with_invalid_method(app):
    @app.route('/invalid', methods=['POST'])
    async def invalid_handler(request):
        return text('invalid')

    with pytest.raises(URLBuildError):
        app.url_for('invalid_handler')