import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.exceptions import URLBuildError
from sanic.response import text
from sanic.constants import HTTP_METHODS

@pytest.mark.parametrize('method', HTTP_METHODS)
def test_url_for_with_invalid_route_name(method):
    app = Sanic("app")
    @app.route('/url-for', methods=[method])
    def url_for_handler(request):
        return text('url-for')

    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")

@pytest.mark.parametrize('method', HTTP_METHODS)
def test_url_for_with_extra_params(method):
    app = Sanic("app")
    @app.route('/url-for', methods=[method], name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    url = app.url_for('url_for_route', extra_param='value')
    assert url == f"/url-for?extra_param=value"

@pytest.mark.parametrize('method', HTTP_METHODS)
def test_url_for_with_versioned_route(method):
    app = Sanic("app")
    @app.route('/v1/url-for', methods=[method], version=1, name='versioned_url_for')
    def versioned_url_for_handler(request):
        return text('versioned url-for')

    url = app.url_for('versioned_url_for')
    assert url == f"/v1/url-for"

@pytest.mark.parametrize('method', HTTP_METHODS)
def test_url_for_with_blueprint(method):
    app = Sanic("app")
    bp = Blueprint("test_bp", url_prefix="/bp")

    @bp.route('/url-for', methods=[method], name='bp_url_for')
    def bp_url_for_handler(request):
        return text('blueprint url-for')

    app.blueprint(bp)

    url = app.url_for('test_bp.bp_url_for')
    assert url == f"/bp/url-for"

@pytest.mark.parametrize('method', HTTP_METHODS)
def test_url_for_with_invalid_param(method):
    app = Sanic("app")
    @app.route('/url-for', methods=[method], name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    with pytest.raises(URLBuildError):
        app.url_for('url_for_route', missing_param='value')