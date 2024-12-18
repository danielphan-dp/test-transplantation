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

def test_url_for_valid_endpoint(app):
    url = app.url_for("url_for")
    assert url == "/url-for"

def test_url_for_with_invalid_endpoint(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("invalid_view")
        assert e.match("Endpoint with name `app.invalid_view` was not found")

def test_url_for_with_query_params(app):
    url = app.url_for("url_for", param1="value1", param2="value2")
    assert url == "/url-for?param1=value1&param2=value2"

def test_url_for_with_external_url(app):
    app.config.update({"SERVER_NAME": "example.com:8000"})
    url = app.url_for("url_for", _external=True)
    assert url == "http://example.com:8000/url-for"

def test_url_for_with_different_schemes(app):
    app.config.update({"SERVER_NAME": "example.com:443"})
    url = app.url_for("url_for", _external=True)
    assert url == "https://example.com:443/url-for"