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
    def user_profile(request, id):
        return text(f'User {id}')

    request, response = app.test_client.get('/user/123')
    assert response.status == 200
    assert response.text == 'User 123'
    assert app.url_for('user_profile', id=123) == '/user/123'

def test_url_for_with_invalid_params(app):
    @app.route('/item/<item_id:int>')
    def item_detail(request, item_id):
        return text(f'Item {item_id}')

    with pytest.raises(URLBuildError):
        app.url_for('item_detail')  # Missing required parameter

def test_url_for_with_multiple_routes(app):
    @app.route('/first', methods=["GET"], name="first_route")
    async def first_handler(request):
        return text("First Route")

    @app.route('/second', methods=["GET"], name="second_route")
    async def second_handler(request):
        return text("Second Route")

    request, response = app.test_client.get(app.url_for("first_route"))
    assert response.text == "First Route"

    request, response = app.test_client.get(app.url_for("second_route"))
    assert response.text == "Second Route"

    assert app.url_for("first_route") == "/first"
    assert app.url_for("second_route") == "/second"