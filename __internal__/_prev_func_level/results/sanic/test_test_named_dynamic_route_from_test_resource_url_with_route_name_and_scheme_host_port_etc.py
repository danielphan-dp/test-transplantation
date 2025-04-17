import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_valid_route(app):
    @app.route('/url-for', name='url_for_route')
    async def url_for_handler(request):
        return text('url-for')

    assert app.url_for('url_for_route') == '/url-for'

def test_url_for_with_query_params(app):
    @app.route('/url-for', name='url_for_route')
    async def url_for_handler(request):
        return text('url-for')

    assert app.url_for('url_for_route', param1='value1', param2='value2') == '/url-for?param1=value1&param2=value2'

def test_url_for_with_nonexistent_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('nonexistent_route')

def test_url_for_with_missing_params(app):
    @app.route('/folder/<name>', name='route_dynamic')
    async def handler(request, name):
        return text("OK")

    with pytest.raises(URLBuildError) as e:
        app.url_for('route_dynamic')  # Missing 'name' parameter
        assert str(e.value) == "Required parameter `name` was not passed to url_for"

def test_url_for_with_dynamic_route(app):
    @app.route('/folder/<name>', name='route_dynamic')
    async def handler(request, name):
        return text("OK")

    assert app.url_for('route_dynamic', name='test') == '/folder/test'