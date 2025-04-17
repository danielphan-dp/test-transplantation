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
        e.match("Endpoint with name `non_existent_route` was not found")

def test_url_for_with_missing_parameters(app):
    @app.route('/user/<id:int>')
    def user(request, id):
        return text(f'User {id}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('user')
        e.match("Required parameter `id` was not passed to url_for")

def test_url_for_with_extra_parameters(app):
    @app.route('/user/<id:int>')
    def user(request, id):
        return text(f'User {id}')

    url = app.url_for('user', id=1, extra_param='extra')
    assert url == '/user/1'

def test_url_for_with_float_parameter(app):
    @app.route('/item/<price:float>')
    def item(request, price):
        return text(f'Item price: {price}')

    url = app.url_for('item', price=19.99)
    assert url == '/item/19.99'

def test_url_for_with_invalid_float_parameter(app):
    @app.route('/item/<price:float>')
    def item(request, price):
        return text(f'Item price: {price}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('item', price='invalid')
        e.match('Value "invalid" for parameter `price` does not match pattern for type `float`')