import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    @app.route('/url-for', name='url_for')
    def url_for(request):
        return text('url-for')
    return app

def test_url_for_with_valid_route(app):
    assert app.url_for('url_for') == '/url-for'

def test_url_for_fails_if_endpoint_not_found(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('non_existent_route')
        e.match("Endpoint with name `test_app.non_existent_route` was not found")

def test_url_for_with_query_params(app):
    @app.route('/url-with-params', name='url_with_params')
    def url_with_params(request):
        return text('url-with-params')
    
    assert app.url_for('url_with_params', param1='value1', param2='value2') == '/url-with-params?param1=value1&param2=value2'

def test_url_for_with_different_http_methods(app):
    @app.route('/get-route', methods=['GET'], name='get_route')
    def get_route(request):
        return text('GET route')

    @app.route('/post-route', methods=['POST'], name='post_route')
    def post_route(request):
        return text('POST route')

    assert app.url_for('get_route') == '/get-route'
    assert app.url_for('post_route') == '/post-route'