import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_valid_route(app):
    @app.route('/url-for', name='url_for_route')
    def url_for(request):
        return text('url-for')

    assert app.url_for('url_for_route') == '/url-for'

def test_url_for_with_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_params(app):
    @app.route('/user/<id>', methods=['GET'], name='user_route')
    def user(request, id):
        return text(f'User {id}')

    assert app.url_for('user_route', id=42) == '/user/42'

def test_url_for_with_multiple_params(app):
    @app.route('/post/<int:post_id>/comment/<int:comment_id>', methods=['GET'], name='comment_route')
    def comment(request, post_id, comment_id):
        return text(f'Post {post_id}, Comment {comment_id}')

    assert app.url_for('comment_route', post_id=1, comment_id=2) == '/post/1/comment/2'

def test_url_for_with_missing_param(app):
    @app.route('/item/<item_id>', methods=['GET'], name='item_route')
    def item(request, item_id):
        return text(f'Item {item_id}')

    with pytest.raises(URLBuildError):
        app.url_for('item_route')