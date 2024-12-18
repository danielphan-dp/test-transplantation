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

def test_url_for_existing_route(app):
    assert app.url_for('url_for') == '/url-for'
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_non_existent_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_query_params(app):
    @app.route('/query', name='query_route')
    def query_route(request):
        return text('query response')

    assert app.url_for('query_route') == '/query'
    request, response = app.test_client.get('/query')
    assert response.status == 200
    assert response.text == 'query response'

def test_url_for_with_blueprint(app):
    bp = Sanic("test_bp", url_prefix="/bp")

    @bp.route('/bp-url', name='bp_url')
    def bp_url(request):
        return text('blueprint url')

    app.blueprint(bp)

    assert app.url_for('bp_url') == '/bp/bp-url'
    request, response = app.test_client.get('/bp/bp-url')
    assert response.status == 200
    assert response.text == 'blueprint url'

def test_url_for_with_invalid_params(app):
    @app.route('/params/<param>', name='params_route')
    def params_route(request, param):
        return text(f'param: {param}')

    with pytest.raises(URLBuildError):
        app.url_for('params_route')  # Missing required parameter

    assert app.url_for('params_route', param='test') == '/params/test'
    request, response = app.test_client.get('/params/test')
    assert response.status == 200
    assert response.text == 'param: test'