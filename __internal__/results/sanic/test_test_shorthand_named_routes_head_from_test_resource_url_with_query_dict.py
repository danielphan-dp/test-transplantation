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
    assert app.url_for('url_for') == '/url-for'

def test_url_for_non_existent_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_query_params(app):
    @app.route('/items', methods=['GET'], name='get_items')
    def get_items(request):
        return text('items list')

    assert app.url_for('get_items') == '/items'
    assert app.url_for('get_items', page=2) == '/items?page=2'

def test_url_for_with_invalid_params(app):
    @app.route('/items/<item_id>', methods=['GET'], name='get_item')
    def get_item(request, item_id):
        return text(f'item {item_id}')

    with pytest.raises(URLBuildError):
        app.url_for('get_item')  # Missing required parameter item_id

def test_url_for_with_multiple_routes(app):
    @app.route('/users', methods=['GET'], name='get_users')
    def get_users(request):
        return text('users list')

    @app.route('/users/<user_id>', methods=['GET'], name='get_user')
    def get_user(request, user_id):
        return text(f'user {user_id}')

    assert app.url_for('get_users') == '/users'
    assert app.url_for('get_user', user_id=1) == '/users/1'