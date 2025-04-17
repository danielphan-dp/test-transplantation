import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route('/url-for', name='url_for')
    def url_for(request):
        return text('url-for')

    return app

def test_url_for_existing_route(app):
    url = app.url_for('url_for')
    assert url == '/url-for'

def test_url_for_with_invalid_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('non_existing_route')
        assert str(e.value) == "Endpoint with name `test_app.non_existing_route` was not found"

def test_url_for_with_query_params(app):
    url = app.url_for('url_for', param1='value1', param2='value2')
    assert url == '/url-for?param1=value1&param2=value2'

def test_url_for_with_server_name(app):
    app.config.update({"SERVER_NAME": "example.com"})
    url = app.url_for('url_for', _external=True)
    assert url == 'http://example.com/url-for'

def test_url_for_with_custom_port(app):
    app.config.update({"SERVER_NAME": "example.com:8080"})
    url = app.url_for('url_for', _external=True)
    assert url == 'http://example.com:8080/url-for'