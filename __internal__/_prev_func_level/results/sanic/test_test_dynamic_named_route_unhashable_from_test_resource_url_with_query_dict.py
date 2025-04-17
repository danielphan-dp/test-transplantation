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

    url = app.url_for('url_for')
    assert url == '/url-for'

def test_url_for_with_nonexistent_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('nonexistent_route')

def test_url_for_with_query_params(app):
    @app.route('/items')
    def items(request):
        return text('items')

    url = app.url_for('items', query={'sort': 'asc'})
    assert url == '/items?sort=asc'

def test_url_for_with_dynamic_route(app):
    @app.route('/user/<user_id:int>')
    def user(request, user_id):
        return text(f'User {user_id}')

    url = app.url_for('user', user_id=42)
    assert url == '/user/42'

def test_url_for_with_missing_param(app):
    @app.route('/post/<post_id:int>')
    def post(request, post_id):
        return text(f'Post {post_id}')

    with pytest.raises(URLBuildError):
        app.url_for('post')