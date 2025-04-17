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

def test_url_for_existing_route(app):
    assert app.url_for('url_for') == '/url-for'

def test_url_for_non_existent_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('non_existent_route')
        assert e.match("Endpoint with name `test_app.non_existent_route` was not found")

def test_url_for_with_query_params(app):
    @app.route('/items', methods=['GET'], name='get_items')
    def get_items(request):
        return text('items list')

    assert app.url_for('get_items') == '/items'
    assert app.url_for('get_items', page=2) == '/items?page=2'

def test_url_for_with_dynamic_route(app):
    @app.route('/user/<user_id>', methods=['GET'], name='get_user')
    def get_user(request, user_id):
        return text(f'User {user_id}')

    assert app.url_for('get_user', user_id=42) == '/user/42'

def test_url_for_with_invalid_param(app):
    @app.route('/product/<product_id>', methods=['GET'], name='get_product')
    def get_product(request, product_id):
        return text(f'Product {product_id}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('get_product')  # Missing required parameter
        assert e.match("Required parameter `product_id` was not passed to url_for")