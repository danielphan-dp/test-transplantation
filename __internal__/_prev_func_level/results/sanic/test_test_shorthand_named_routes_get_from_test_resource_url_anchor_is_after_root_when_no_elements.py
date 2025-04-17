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
    @app.route('/query', methods=['GET'], name='query_route')
    def query_handler(request):
        return text('query response')

    assert app.url_for('query_route') == '/query'
    assert app.url_for('query_route', param1='value1') == '/query?param1=value1'

def test_url_for_with_blueprint(app):
    from sanic.blueprints import Blueprint
    bp = Blueprint("test_bp", url_prefix="/bp")

    @bp.route('/bp-url', name='bp_route')
    def bp_handler(request):
        return text('blueprint url')

    app.blueprint(bp)

    assert app.url_for('bp_route') == '/bp/bp-url'

def test_url_for_with_invalid_params(app):
    @app.route('/params/<param>', methods=['GET'], name='params_route')
    def params_handler(request, param):
        return text(f'param: {param}')

    with pytest.raises(URLBuildError):
        app.url_for('params_route')  # Missing required parameter

    assert app.url_for('params_route', param='test') == '/params/test'