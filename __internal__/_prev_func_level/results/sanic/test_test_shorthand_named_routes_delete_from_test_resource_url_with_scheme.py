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

    assert app.url_for('query_route', param1='value1', param2='value2') == '/query?param1=value1&param2=value2'

def test_url_for_with_different_http_methods(app):
    @app.post('/post-route', name='post_route')
    def post_handler(request):
        return text('post response')

    assert app.url_for('post_route') == '/post-route'