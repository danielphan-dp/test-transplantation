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

    assert app.url_for('url_for') == '/url-for'
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_nonexistent_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('nonexistent_route')

def test_url_for_with_query_params(app):
    @app.route('/user/<id>')
    def user_handler(request, id):
        return text(f'User ID: {id}')

    assert app.url_for('user_handler', id=42) == '/user/42'
    request, response = app.test_client.get('/user/42')
    assert response.status == 200
    assert response.text == 'User ID: 42'

def test_url_for_with_missing_params(app):
    @app.route('/item/<item_id>')
    def item_handler(request, item_id):
        return text(f'Item ID: {item_id}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('item_handler')
        assert e.match("Required parameter `item_id` was not passed to url_for")