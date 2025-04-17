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
def test_url_for_with_query_parameters(method):
    app = Sanic("app")
    @app.route('/url-for', methods=[method])
    def url_for_handler(request):
        return text('url-for')

    url = app.url_for("url-for", param1="value1", param2="value2")
    assert url == f"/url-for?param1=value1&param2=value2"

@pytest.mark.parametrize('method', HTTP_METHODS)
def test_url_for_with_versioned_routes(method):
    app = Sanic("app")
    bp = Blueprint("test_bp", url_prefix="/bp")

    @app.route(f"/{method}", version=1, name=f"route_{method}")
    def handler(request):
        return text("OK")

    @bp.route(f"/{method}", version=1, name=f"route2_{method}")
    def handler2(request):
        return text("OK")

    app.blueprint(bp)

    assert app.url_for(f"route_{method}") == f"/v1/{method}"
    assert app.url_for(f"test_bp.route2_{method}") == f"/v1/bp/{method}"

@pytest.mark.parametrize('method', HTTP_METHODS)
def test_url_for_with_missing_parameters(method):
    app = Sanic("app")
    @app.route(f"/{method}/<param>", methods=[method])
    def handler(request, param):
        return text("OK")

    with pytest.raises(URLBuildError) as e:
        app.url_for(f"handler")
        assert "Required parameter" in str(e.value)