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

def test_url_for_with_dynamic_route(app):
    @app.route('/dynamic/<name>')
    def dynamic_handler(request, name):
        return text(f'Hello, {name}')

    assert app.url_for('dynamic_handler', name='John') == '/dynamic/John'

def test_url_for_with_missing_params(app):
    @app.route('/greet/<name>')
    def greet_handler(request, name):
        return text(f'Hello, {name}')

    with pytest.raises(URLBuildError):
        app.url_for('greet_handler')