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

def test_url_for_valid_route(app):
    assert app.url_for('url_for') == '/url-for'

def test_url_for_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_params(app):
    @app.route('/user/<id>', methods=['GET'], name='user_profile')
    def user_profile(request, id):
        return text(f'User {id}')

    assert app.url_for('user_profile', id=42) == '/user/42'

def test_url_for_with_missing_param(app):
    @app.route('/item/<item_id>', methods=['GET'], name='item_detail')
    def item_detail(request, item_id):
        return text(f'Item {item_id}')

    with pytest.raises(URLBuildError):
        app.url_for('item_detail')