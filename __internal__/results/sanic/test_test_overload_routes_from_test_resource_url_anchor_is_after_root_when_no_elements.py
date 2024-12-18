import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")

def test_url_for_with_params(app):
    @app.route('/user/<id:int>', methods=["GET"], name="user_route")
    async def user_handler(request, id):
        return text(f'User ID: {id}')

    request, response = app.test_client.get(app.url_for("user_route", id=42))
    assert response.status == 200
    assert response.text == 'User ID: 42'

def test_url_for_with_multiple_routes(app):
    @app.route('/item', methods=["GET"], name="item_route")
    async def item_handler(request):
        return text('Item')

    @app.route('/item/<id:int>', methods=["GET"], name="item_detail_route")
    async def item_detail_handler(request, id):
        return text(f'Item ID: {id}')

    assert app.url_for("item_route") == "/item"
    assert app.url_for("item_detail_route", id=5) == "/item/5"

def test_url_for_with_query_params(app):
    @app.route('/search', methods=["GET"], name="search_route")
    async def search_handler(request):
        query = request.args.get('query', '')
        return text(f'Search query: {query}')

    request, response = app.test_client.get(app.url_for("search_route", query="test"))
    assert response.status == 200
    assert response.text == 'Search query: test'