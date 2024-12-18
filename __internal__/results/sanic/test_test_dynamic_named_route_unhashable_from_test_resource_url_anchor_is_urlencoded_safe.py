import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

def test_url_for_basic(app):
    @app.route('/url-for', name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    url = app.url_for('url_for_route')
    assert url == '/url-for'

def test_url_for_with_params(app):
    @app.route('/user/<id:int>', name='user_route')
    def user_handler(request, id):
        return text(f'User {id}')

    url = app.url_for('user_route', id=42)
    assert url == '/user/42'

def test_url_for_fails_if_endpoint_not_found(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('non_existent_route')
        e.match("Endpoint with name `app.non_existent_route` was not found")

def test_url_for_with_invalid_params(app):
    @app.route('/item/<item_id:int>', name='item_route')
    def item_handler(request, item_id):
        return text(f'Item {item_id}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('item_route', item_id='invalid')
        e.match("Required parameter `item_id` was not passed to url_for")