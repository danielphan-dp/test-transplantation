import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_returns_correct_url(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    expected_url = 'http://localhost:8000/url-for'
    assert expected_url == app.url_for('url_for', _external=True)

def test_url_for_with_invalid_param(app):
    @app.route('/url-for/<param>')
    def url_for_with_param(request, param):
        return text(param)

    with pytest.raises(URLBuildError) as e:
        app.url_for('url_for_with_param', invalid_param='test')
        e.match("Required parameter `param` was not passed to url_for")

def test_url_for_with_missing_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('non_existent_route')
        e.match("Endpoint with name `app.non_existent_route` was not found")

def test_url_for_with_query_params(app):
    @app.route('/url-for')
    def url_for_with_query(request):
        return text('url-for with query')

    expected_url = 'http://localhost:8000/url-for?foo=bar'
    assert expected_url == app.url_for('url_for_with_query', foo='bar', _external=True)

def test_url_for_with_special_characters(app):
    @app.route('/url-for/<name>')
    def url_for_with_special_char(request, name):
        return text(name)

    expected_url = 'http://localhost:8000/url-for/test%20name'
    assert expected_url == app.url_for('url_for_with_special_char', name='test name', _external=True)