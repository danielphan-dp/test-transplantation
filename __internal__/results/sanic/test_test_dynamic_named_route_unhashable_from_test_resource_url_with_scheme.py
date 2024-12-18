import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

def test_url_for_basic(app):
    @app.route('/url-for')
    def url_for_handler(request):
        return text('url-for')

    url = app.url_for('url_for_handler')
    assert url == '/url-for'

def test_url_for_with_invalid_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('non_existent_handler')
        e.match("Endpoint with name `app.non_existent_handler` was not found")

def test_url_for_with_query_params(app):
    @app.route('/url-for')
    def url_for_handler(request):
        return text('url-for')

    url = app.url_for('url_for_handler', param1='value1', param2='value2')
    assert url == '/url-for?param1=value1&param2=value2'

def test_url_for_with_dynamic_route(app):
    @app.route('/folder/<name>/end/', name='dynamic_route')
    async def dynamic_handler(request, name):
        return text(f'Hello {name}')

    url = app.url_for('dynamic_route', name='test')
    assert url == '/folder/test/end/'

def test_url_for_with_missing_params(app):
    @app.route('/folder/<name>/end/', name='dynamic_route')
    async def dynamic_handler(request, name):
        return text(f'Hello {name}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('dynamic_route')
        e.match("Required parameter `name` was not passed to url_for")