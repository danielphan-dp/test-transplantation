import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_valid_route(app):
    @app.route('/url-for', name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    url = app.url_for('url_for_route')
    assert url == '/url-for'

def test_url_for_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_params(app):
    @app.route('/user/<user_id>', name='user_route')
    def user_handler(request, user_id):
        return text(f'User ID: {user_id}')

    url = app.url_for('user_route', user_id='123')
    assert url == '/user/123'

def test_url_for_with_missing_param(app):
    @app.route('/item/<item_id>', name='item_route')
    def item_handler(request, item_id):
        return text(f'Item ID: {item_id}')

    with pytest.raises(URLBuildError):
        app.url_for('item_route')