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
def test_url_for_with_params(method):
    app = Sanic("app")
    
    @app.route(f"/{method}/<param>", methods=[method])
    def param_handler(request, param):
        return text(f"Received param: {param}")

    url = app.url_for(f"param_handler", param="test")
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "Received param: test"

@pytest.mark.parametrize('method', HTTP_METHODS)
def test_url_for_with_multiple_params(method):
    app = Sanic("app")
    
    @app.route(f"/{method}/<param1>/<param2>", methods=[method])
    def multi_param_handler(request, param1, param2):
        return text(f"Received params: {param1}, {param2}")

    url = app.url_for("multi_param_handler", param1="test1", param2="test2")
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "Received params: test1, test2"

@pytest.mark.parametrize('method', HTTP_METHODS)
def test_url_for_with_query_params(method):
    app = Sanic("app")
    
    @app.route(f"/{method}/query", methods=[method])
    def query_handler(request):
        return text(f"Query: {request.args}")

    url = app.url_for("query_handler", _external=True, param1="value1", param2="value2")
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert "Query: {'param1': ['value1'], 'param2': ['value2']}" in response.text

@pytest.mark.parametrize('method', HTTP_METHODS)
def test_url_for_with_invalid_param(method):
    app = Sanic("app")
    
    @app.route(f"/{method}/<param>", methods=[method])
    def param_handler(request, param):
        return text(f"Received param: {param}")

    with pytest.raises(URLBuildError):
        app.url_for("param_handler")  # Missing required param

@pytest.mark.parametrize('method', HTTP_METHODS)
def test_url_for_with_nonexistent_blueprint_route(method):
    app = Sanic("app")
    bp = Blueprint("test_bp", url_prefix="/bp")

    @bp.route(f"/{method}", methods=[method])
    def bp_handler(request):
        return text("Blueprint OK")

    app.blueprint(bp)

    with pytest.raises(URLBuildError):
        app.url_for("nonexistent_bp_route")  # Non-existent route in blueprint