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

    @bp.route('/url-for', name='url_for_bp_route')
    def url_for_bp_handler(request):
        return text('url-for bp')

    app.blueprint(bp)

    assert app.url_for('test_bp.url_for_bp_route') == '/bp/url-for'

def test_url_for_with_params(app):
    @app.route('/url-for/<param>', name='url_for_param_route')
    def url_for_param_handler(request, param):
        return text(f'url-for with param: {param}')

    assert app.url_for('url_for_param_route', param='test') == '/url-for/test'

def test_url_for_with_missing_param(app):
    @app.route('/url-for/<param>', name='url_for_param_route')
    def url_for_param_handler(request, param):
        return text(f'url-for with param: {param}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('url_for_param_route')
        assert str(e.value) == "Required parameter `param` was not passed to url_for"