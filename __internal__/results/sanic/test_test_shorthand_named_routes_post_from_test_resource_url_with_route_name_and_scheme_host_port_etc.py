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

def test_url_for_with_valid_route(app):
    assert app.url_for('url_for_route') == '/url-for'
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_query_params(app):
    @app.route('/url-for/<param>', name='url_for_with_param')
    def param_handler(request, param):
        return text(f'param: {param}')

    assert app.url_for('url_for_with_param', param='test') == '/url-for/test'
    request, response = app.test_client.get('/url-for/test')
    assert response.status == 200
    assert response.text == 'param: test'

def test_url_for_with_multiple_params(app):
    @app.route('/url-for/<param1>/<param2>', name='url_for_multiple_params')
    def multi_param_handler(request, param1, param2):
        return text(f'param1: {param1}, param2: {param2}')

    assert app.url_for('url_for_multiple_params', param1='test1', param2='test2') == '/url-for/test1/test2'
    request, response = app.test_client.get('/url-for/test1/test2')
    assert response.status == 200
    assert response.text == 'param1: test1, param2: test2'

def test_url_for_with_missing_param(app):
    @app.route('/url-for/<param>', name='url_for_missing_param')
    def missing_param_handler(request, param):
        return text(f'param: {param}')

    with pytest.raises(URLBuildError):
        app.url_for('url_for_missing_param')