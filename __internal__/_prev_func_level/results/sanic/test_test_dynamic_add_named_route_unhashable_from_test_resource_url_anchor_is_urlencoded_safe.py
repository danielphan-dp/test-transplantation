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

    url = app.url_for('url_for_route')
    assert url == '/url-for'

def test_url_for_with_nonexistent_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('nonexistent_route')
        assert str(e.value) == "Endpoint with name `app.nonexistent_route` was not found"

def test_url_for_with_parameters(app):
    @app.route('/user/<id:int>', name='user_route')
    def user(request, id):
        return text(f'User {id}')

    url = app.url_for('user_route', id=42)
    assert url == '/user/42'

def test_url_for_with_invalid_parameters(app):
    @app.route('/item/<item_id:int>', name='item_route')
    def item(request, item_id):
        return text(f'Item {item_id}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('item_route')  # Missing required parameter
        assert str(e.value) == "Required parameter `item_id` was not passed to url_for"