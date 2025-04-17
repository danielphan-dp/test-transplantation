import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/url-for")
    def url_for(request):
        return text('url-for')

    return app

def test_url_for_with_valid_endpoint(app):
    url = app.url_for("url-for")
    assert url == "/url-for"

def test_url_for_with_nonexistent_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("nonexistent")
        e.match("Endpoint with name `app.nonexistent` was not found")

def test_url_for_with_additional_params(app):
    @app.route("/params/<param>")
    def params(request, param):
        return text(f'param: {param}')

    url = app.url_for("params", param="test")
    assert url == "/params/test"

def test_url_for_with_invalid_param(app):
    @app.route("/params/<param>")
    def params(request, param):
        return text(f'param: {param}')

    with pytest.raises(URLBuildError) as e:
        app.url_for("params")
        e.match("Required parameter `param` was not passed to url_for")