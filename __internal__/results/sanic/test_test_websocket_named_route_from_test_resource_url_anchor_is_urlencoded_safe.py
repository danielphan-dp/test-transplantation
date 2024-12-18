import asyncio
import pytest
from sanic import Sanic
from sanic.exceptions import URLBuildError
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_valid_route(app):
    @app.route('/url-for', name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    assert app.url_for('url_for_route') == '/url-for'
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_query_params(app):
    @app.route('/url-for', name='url_for_route_with_params')
    def url_for_handler(request):
        return text('url-for with params')

    url = app.url_for('url_for_route_with_params', param1='value1', param2='value2')
    assert url == '/url-for?param1=value1&param2=value2'
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for with params'

def test_url_for_with_invalid_params(app):
    @app.route('/url-for', name='url_for_route_invalid_params')
    def url_for_handler(request):
        return text('url-for with invalid params')

    with pytest.raises(URLBuildError):
        app.url_for('url_for_route_invalid_params', missing_param='value')