import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_basic(app):
    @app.route('/url-for', name='url_for')
    def url_for(request):
        return text('url-for')

    assert app.url_for('url_for') == '/url-for'
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_nonexistent_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('nonexistent_route')

def test_url_for_with_query_params(app):
    @app.route('/url-for', methods=['GET'], name='url_for_with_params')
    def url_for_with_params(request):
        return text('url-for with params')

    assert app.url_for('url_for_with_params', param1='value1', param2='value2') == '/url-for?param1=value1&param2=value2'
    request, response = app.test_client.get('/url-for?param1=value1&param2=value2')
    assert response.status == 200
    assert response.text == 'url-for with params'

def test_url_for_with_invalid_params(app):
    @app.route('/url-for', name='url_for_invalid')
    def url_for_invalid(request):
        return text('url-for invalid')

    with pytest.raises(URLBuildError):
        app.url_for('url_for_invalid', invalid_param='value')