import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    return app

def test_url_for_endpoint(app):
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_invalid_endpoint(app):
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")

def test_url_for_with_params(app):
    @app.route('/user/<id:int>')
    def user_handler(request, id):
        return text(f'User ID: {id}')

    request, response = app.test_client.get('/user/123')
    assert response.status == 200
    assert response.text == 'User ID: 123'
    assert app.url_for('user_handler', id=123) == '/user/123'

def test_url_for_with_query_params(app):
    @app.route('/search')
    def search_handler(request):
        query = request.args.get('query', '')
        return text(f'Search query: {query}')

    request, response = app.test_client.get('/search?query=test')
    assert response.status == 200
    assert response.text == 'Search query: test'
    assert app.url_for('search_handler', query='test') == '/search?query=test'

def test_url_for_with_invalid_params(app):
    @app.route('/item/<item_id:int>')
    def item_handler(request, item_id):
        return text(f'Item ID: {item_id}')

    with pytest.raises(URLBuildError):
        app.url_for('item_handler', item_id='invalid')