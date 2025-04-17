import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route('/url-for', name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    return app

def test_url_for_with_valid_route(app):
    assert app.url_for('url_for_route') == '/url-for'

def test_url_for_with_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_additional_params(app):
    @app.route('/user/<id>', name='user_route')
    def user_handler(request, id):
        return text(f'User {id}')

    assert app.url_for('user_route', id=42) == '/user/42'

def test_url_for_with_missing_params(app):
    @app.route('/item/<item_id>', name='item_route')
    def item_handler(request, item_id):
        return text(f'Item {item_id}')

    with pytest.raises(URLBuildError):
        app.url_for('item_route')