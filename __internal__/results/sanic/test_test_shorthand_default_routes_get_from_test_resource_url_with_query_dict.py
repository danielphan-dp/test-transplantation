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
        app.url_for('non_existent')
        assert str(e.value) == "Endpoint with name `test_app.non_existent` was not found"

def test_url_for_with_query_params(app):
    @app.route('/items', name='items')
    def items(request):
        return text('items list')

    assert app.url_for('items') == '/items'
    assert app.url_for('items', page=2) == '/items?page=2'

def test_url_for_with_multiple_params(app):
    @app.route('/user/<id>', name='user_profile')
    def user_profile(request, id):
        return text(f'User {id}')

    assert app.url_for('user_profile', id=42) == '/user/42'

def test_url_for_with_invalid_param(app):
    @app.route('/product/<slug>', name='product_detail')
    def product_detail(request, slug):
        return text(f'Product {slug}')

    assert app.url_for('product_detail', slug='test-product') == '/product/test-product'