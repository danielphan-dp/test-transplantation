import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route('/url-for', name='url_for_route')
    async def url_for_handler(request):
        return text('url-for')

    return app

def test_url_for_with_valid_route(app):
    assert app.url_for('url_for_route') == '/url-for'

def test_url_for_with_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_query_params(app):
    @app.route('/items/<item_id>', name='item_route')
    async def item_handler(request, item_id):
        return text(f'Item {item_id}')

    assert app.url_for('item_route', item_id='123') == '/items/123'

def test_url_for_with_missing_params(app):
    @app.route('/user/<user_id>', name='user_route')
    async def user_handler(request, user_id):
        return text(f'User {user_id}')

    with pytest.raises(URLBuildError):
        app.url_for('user_route')  # Missing user_id

def test_url_for_with_special_characters(app):
    @app.route('/folder/<folder_id:[A-Za-z0-9]{0,4}>', name='folder_route')
    async def folder_handler(request, folder_id):
        return text(f'Folder {folder_id}')

    assert app.url_for('folder_route', folder_id='test') == '/folder/test'
    with pytest.raises(URLBuildError):
        app.url_for('folder_route', folder_id='invalid_folder_id')  # Invalid folder_id length

def test_url_for_with_multiple_params(app):
    @app.route('/post/<post_id>/comment/<comment_id>', name='comment_route')
    async def comment_handler(request, post_id, comment_id):
        return text(f'Post {post_id}, Comment {comment_id}')

    assert app.url_for('comment_route', post_id='1', comment_id='2') == '/post/1/comment/2'