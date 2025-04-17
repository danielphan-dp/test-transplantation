import pytest
from sanic import Sanic, Blueprint
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

def test_url_for_with_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_blueprint(app):
    bp = Blueprint("test_bp", url_prefix="/bp")

    @bp.get("/url-for", name="bp_url_for_route")
    def bp_url_for_handler(request):
        return text('blueprint url-for')

    app.blueprint(bp)

    assert app.url_for("bp_url_for_route") == "/bp/url-for"

def test_url_for_with_query_parameters(app):
    @app.route('/url-for', methods=['GET'], name='url_for_route_with_query')
    def url_for_handler_with_query(request):
        return text('url-for with query')

    expected_url = '/url-for?param=value'
    assert app.url_for('url_for_route_with_query', param='value') == expected_url

def test_url_for_with_missing_parameters(app):
    @app.route('/url-for/<param>', methods=['GET'], name='url_for_route_with_param')
    def url_for_handler_with_param(request, param):
        return text(f'url-for with param: {param}')

    with pytest.raises(URLBuildError):
        app.url_for('url_for_route_with_param')