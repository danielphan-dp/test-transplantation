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
    assert app.url_for("url_for_route") == "/url-for"

def test_url_for_non_existent_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_route")
        assert str(e.value) == "Endpoint with name `test_app.non_existent_route` was not found"

def test_url_for_with_query_params(app):
    @app.route('/query', name='query_route')
    def query_handler(request):
        return text('query response')

    assert app.url_for("query_route", param1="value1", param2="value2") == "/query?param1=value1&param2=value2"

def test_url_for_with_path_params(app):
    @app.route('/path/<param>', name='path_route')
    def path_handler(request, param):
        return text(f'Path param: {param}')

    assert app.url_for("path_route", param="test") == "/path/test"

def test_url_for_with_invalid_param(app):
    @app.route('/invalid/<param>', name='invalid_route')
    def invalid_handler(request, param):
        return text(f'Invalid param: {param}')

    with pytest.raises(URLBuildError) as e:
        app.url_for("invalid_route")
        assert str(e.value) == "Required parameter `param` was not passed to url_for"