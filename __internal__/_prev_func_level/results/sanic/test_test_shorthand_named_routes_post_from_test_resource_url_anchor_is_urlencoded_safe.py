import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route('/url-for', name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    return app

def test_url_for_existing_route(app):
    assert app.url_for('url_for_route') == '/url-for'

def test_url_for_non_existent_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_query_params(app):
    @app.route('/query', methods=['GET'], name='query_route')
    def query_handler(request):
        return text('query response')

    assert app.url_for('query_route') == '/query'
    assert app.url_for('query_route', param='value') == '/query?param=value'

def test_url_for_with_multiple_routes(app):
    @app.route('/first', methods=['GET'], name='first_route')
    def first_handler(request):
        return text('first response')

    @app.route('/second', methods=['GET'], name='second_route')
    def second_handler(request):
        return text('second response')

    assert app.url_for('first_route') == '/first'
    assert app.url_for('second_route') == '/second'

def test_url_for_with_invalid_method(app):
    @app.route('/invalid', methods=['POST'], name='invalid_route')
    def invalid_handler(request):
        return text('invalid response')

    with pytest.raises(URLBuildError):
        app.url_for('invalid_route', _method='GET')