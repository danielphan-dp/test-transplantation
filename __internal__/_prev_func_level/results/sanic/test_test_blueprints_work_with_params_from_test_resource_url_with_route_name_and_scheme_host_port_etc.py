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
    expected_url = '/url-for'
    assert expected_url == app.url_for('url_for')

def test_url_for_with_invalid_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_endpoint")
        assert e.match("Endpoint with name `app.non_existent_endpoint` was not found")

def test_url_for_with_params(app):
    @app.route('/params/<param>')
    def params_view(request, param):
        return text(f'param: {param}')

    expected_url = '/params/test'
    assert expected_url == app.url_for('params_view', param='test')

def test_url_for_with_query_params(app):
    @app.route('/query')
    def query_view(request):
        return text('query')

    expected_url = '/query?key=value'
    assert expected_url == app.url_for('query_view', _query={'key': 'value'})

def test_url_for_with_server_name(app):
    app.config.update({"SERVER_NAME": "example.com"})
    expected_url = 'http://example.com/url-for'
    assert expected_url == app.url_for('url_for', _external=True)

def test_url_for_with_different_schemes(app):
    app.config.update({"SERVER_NAME": "example.com"})
    expected_http_url = 'http://example.com/url-for'
    expected_https_url = 'https://example.com/url-for'
    assert expected_http_url == app.url_for('url_for', _external=True, _scheme='http')
    assert expected_https_url == app.url_for('url_for', _external=True, _scheme='https')