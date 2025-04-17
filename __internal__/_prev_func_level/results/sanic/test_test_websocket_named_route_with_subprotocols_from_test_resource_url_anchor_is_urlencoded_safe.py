import pytest
from sanic import Sanic
from sanic.exceptions import URLBuildError
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_valid_route(app):
    @app.route('/url-for', name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    assert app.url_for('url_for_route') == '/url-for'
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_nonexistent_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('nonexistent_route')

def test_url_for_with_parameters(app):
    @app.route('/user/<id>', methods=['GET'], name='user_route')
    def user_handler(request, id):
        return text(f'User ID: {id}')

    assert app.url_for('user_route', id=42) == '/user/42'
    request, response = app.test_client.get('/user/42')
    assert response.status == 200
    assert response.text == 'User ID: 42'

def test_url_for_with_missing_parameters(app):
    @app.route('/user/<id>', methods=['GET'], name='user_route')
    def user_handler(request, id):
        return text(f'User ID: {id}')

    with pytest.raises(URLBuildError):
        app.url_for('user_route')