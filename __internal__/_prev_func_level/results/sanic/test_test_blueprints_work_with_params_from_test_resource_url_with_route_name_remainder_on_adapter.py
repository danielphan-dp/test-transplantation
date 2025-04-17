import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')
    return app

def test_url_for_basic(app):
    url = app.url_for("url_for")
    assert url == "/url-for"

def test_url_for_with_invalid_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_endpoint")
        assert e.match("Endpoint with name `app.non_existent_endpoint` was not found")

def test_url_for_with_params(app):
    @app.route('/params/<param>')
    def params_view(request, param):
        return text(f'param: {param}')

    url = app.url_for("params_view", param="test")
    assert url == "/params/test"

def test_url_for_with_multiple_params(app):
    @app.route('/multi/<param1>/<param2>')
    def multi_params_view(request, param1, param2):
        return text(f'param1: {param1}, param2: {param2}')

    url = app.url_for("multi_params_view", param1="foo", param2="bar")
    assert url == "/multi/foo/bar"

def test_url_for_with_missing_param(app):
    @app.route('/missing/<param>')
    def missing_param_view(request, param):
        return text(f'param: {param}')

    with pytest.raises(URLBuildError) as e:
        app.url_for("missing_param_view")
        assert e.match("Required parameter `param` was not passed to url_for")