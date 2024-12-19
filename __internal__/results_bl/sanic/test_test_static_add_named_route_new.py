import asyncio
import pytest
from sanic import Sanic
from sanic.exceptions import URLBuildError
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("app")
    return app

@app.route('/url-for')
def url_for(request):
    return text('url-for')

def test_url_for_route(app):
    @app.route('/test-url')
    def test_url(request):
        return text("Test URL")

    assert app.url_for('test_url') == '/test-url'
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_query_params(app):
    @app.route('/test-url/<param>')
    def test_url_with_param(request, param):
        return text(f"Param: {param}")

    assert app.url_for('test_url_with_param', param='value') == '/test-url/value'
    with pytest.raises(URLBuildError):
        app.url_for('test_url_with_param')  # Missing required parameter

def test_url_for_with_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('invalid_route_name')  # Testing invalid route name

def test_url_for_static_route(app):
    @app.route('/static-url', methods=['GET'], name='static_route')
    def static_route(request):
        return text("Static URL")

    assert app.url_for('static_route') == '/static-url'