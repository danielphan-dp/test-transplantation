import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_basic(app):
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

def test_url_for_with_query_params(app):
    @app.route('/url-for/<param>', name='url_for_with_param')
    def url_for_with_param_handler(request, param):
        return text(f'url-for with param: {param}')

    assert app.url_for('url_for_with_param', param='test') == '/url-for/test'
    request, response = app.test_client.get('/url-for/test')
    assert response.status == 200
    assert response.text == 'url-for with param: test'

def test_url_for_with_missing_param(app):
    @app.route('/url-for/<param>', name='url_for_with_param')
    def url_for_with_param_handler(request, param):
        return text(f'url-for with param: {param}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('url_for_with_param')
        assert str(e.value) == "Required parameter `param` was not passed to url_for"