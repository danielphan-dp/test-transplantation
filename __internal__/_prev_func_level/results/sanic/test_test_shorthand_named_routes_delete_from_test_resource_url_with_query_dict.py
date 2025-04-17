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
    @app.route('/query', name='query_route')
    def query_handler(request):
        return text('query response')

    assert app.url_for('query_route') == '/query'
    assert app.url_for('query_route', param='value') == '/query?param=value'

def test_url_for_with_multiple_params(app):
    @app.route('/multi/<param1>/<param2>', name='multi_param_route')
    def multi_param_handler(request, param1, param2):
        return text(f'param1: {param1}, param2: {param2}')

    assert app.url_for('multi_param_route', param1='value1', param2='value2') == '/multi/value1/value2'

def test_url_for_with_missing_param(app):
    @app.route('/missing/<param>', name='missing_param_route')
    def missing_param_handler(request, param):
        return text(param)

    with pytest.raises(URLBuildError):
        app.url_for('missing_param_route')