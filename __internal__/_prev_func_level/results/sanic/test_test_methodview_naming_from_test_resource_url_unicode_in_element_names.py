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

def test_url_for_valid(app):
    url = app.url_for("url_for")
    assert url == "/url-for"

def test_url_for_with_invalid_view(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_view")
        assert e.match("Endpoint with name `non_existent_view` was not found")

def test_url_for_with_query_params(app):
    url = app.url_for("url_for", param1="value1", param2="value2")
    assert url == "/url-for?param1=value1&param2=value2"

def test_url_for_with_server_name(app):
    server_name = "example.com:8000"
    app.config.update({"SERVER_NAME": server_name})
    url = app.url_for("url_for", _external=True)
    assert url == f"http://{server_name}/url-for"

def test_url_for_with_different_schemes(app):
    app.config.update({"SERVER_NAME": "example.com"})
    url_http = app.url_for("url_for", _external=True, _scheme="http")
    url_https = app.url_for("url_for", _external=True, _scheme="https")
    assert url_http == "http://example.com/url-for"
    assert url_https == "https://example.com/url-for"