import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_basic(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    assert app.url_for('url_for') == '/url-for'
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_nonexistent_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('nonexistent_route')
        assert e.match("Endpoint with name `test_app.nonexistent_route` was not found")

def test_url_for_with_query_params(app):
    @app.route('/url-for/<name>')
    def url_for_with_params(request, name):
        return text(f'Hello, {name}')

    assert app.url_for('url_for_with_params', name='test') == '/url-for/test'
    request, response = app.test_client.get('/url-for/test')
    assert response.status == 200
    assert response.text == 'Hello, test'

def test_url_for_with_missing_params(app):
    @app.route('/url-for/<name>')
    def url_for_with_missing_params(request, name):
        return text(f'Hello, {name}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('url_for_with_missing_params')
        assert e.match("Required parameter `name` was not passed to url_for")