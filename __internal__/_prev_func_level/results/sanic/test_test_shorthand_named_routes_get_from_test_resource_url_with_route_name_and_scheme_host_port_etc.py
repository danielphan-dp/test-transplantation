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

def test_url_for_with_query_params(app):
    @app.route('/url-for', name='url_for_route_with_params')
    def url_for_handler(request):
        return text('url-for with params')

    assert app.url_for('url_for_route_with_params', param1='value1', param2='value2') == '/url-for?param1=value1&param2=value2'

def test_url_for_with_invalid_params(app):
    @app.route('/url-for/<param>', name='url_for_route_with_param')
    def url_for_handler(request, param):
        return text(f'url-for with param: {param}')

    with pytest.raises(URLBuildError):
        app.url_for('url_for_route_with_param')  # Missing required parameter

def test_url_for_with_different_http_methods(app):
    @app.route('/url-for', methods=['POST'], name='url_for_post_route')
    def url_for_post_handler(request):
        return text('url-for post')

    assert app.url_for('url_for_post_route') == '/url-for'