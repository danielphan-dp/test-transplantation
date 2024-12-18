import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@app.route('/url-for', name='url_for_route')
def url_for(request):
    return text('url-for')

def test_url_for_existing_route(app):
    @app.route('/test-route', name='test_route')
    async def test_handler(request):
        return text("Test Route")

    assert app.url_for('test_route') == '/test-route'

def test_url_for_non_existent_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_params(app):
    @app.route('/user/<id>', methods=['GET'], name='user_route')
    async def user_handler(request, id):
        return text(f"User ID: {id}")

    assert app.url_for('user_route', id=123) == '/user/123'

def test_url_for_with_invalid_params(app):
    @app.route('/item/<item_id>', methods=['GET'], name='item_route')
    async def item_handler(request, item_id):
        return text(f"Item ID: {item_id}")

    with pytest.raises(URLBuildError):
        app.url_for('item_route')  # Missing required parameter

def test_url_for_with_query_params(app):
    @app.route('/search', methods=['GET'], name='search_route')
    async def search_handler(request):
        return text("Search")

    assert app.url_for('search_route', query='test') == '/search?query=test'