import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_valid_route(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    expected_url = '/url-for'
    assert expected_url == app.url_for('url_for')

def test_url_for_with_invalid_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('non_existent_route')
        e.match("Endpoint with name `app.non_existent_route` was not found")

def test_url_for_with_missing_param(app):
    @app.route('/user/<id:int>')
    def user(request, id):
        return text(f'User {id}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('user')
        e.match("Required parameter `id` was not passed to url_for")

def test_url_for_with_invalid_param(app):
    @app.route('/user/<username:str>')
    def user(request, username):
        return text(f'User {username}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('user', username='123')
        e.match('Value "123" for parameter `username` does not satisfy pattern ^[A-z]+$')

def test_url_for_with_extra_params(app):
    @app.route('/item/<item_id:int>')
    def item(request, item_id):
        return text(f'Item {item_id}')

    expected_url = '/item/42?extra_param=value'
    assert expected_url == app.url_for('item', item_id=42, extra_param='value')