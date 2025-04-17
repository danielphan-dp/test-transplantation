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
    def url_for_handler(request):
        return text('url-for')

    assert app.url_for('url_for_route') == '/url-for'
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_nonexistent_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('nonexistent_route')

def test_url_for_with_query_parameters(app):
    @app.route('/url-for', methods=['GET'], name='url_for_route_with_query')
    def url_for_handler(request):
        return text('url-for with query')

    url = app.url_for('url_for_route_with_query', param1='value1', param2='value2')
    assert url == '/url-for?param1=value1&param2=value2'
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for with query'

def test_url_for_with_invalid_parameters(app):
    @app.route('/url-for/<param>', methods=['GET'], name='url_for_route_with_param')
    def url_for_handler(request, param):
        return text(f'url-for with param: {param}')

    with pytest.raises(URLBuildError):
        app.url_for('url_for_route_with_param')  # Missing required parameter

    url = app.url_for('url_for_route_with_param', param='test')
    assert url == '/url-for/test'
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for with param: test'