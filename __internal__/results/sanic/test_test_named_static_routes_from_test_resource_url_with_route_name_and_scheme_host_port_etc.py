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

def test_url_for_with_valid_route(app):
    assert app.url_for('url_for') == '/url-for'

def test_url_for_with_invalid_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_query_parameters(app):
    @app.route('/query', name='query_route')
    async def query_handler(request):
        return text('query response')

    assert app.url_for('query_route') == '/query'
    assert app.url_for('query_route', param1='value1') == '/query?param1=value1'

def test_url_for_with_multiple_routes(app):
    @app.route('/first', name='first_route')
    async def first_handler(request):
        return text('first response')

    @app.route('/second', name='second_route')
    async def second_handler(request):
        return text('second response')

    assert app.url_for('first_route') == '/first'
    assert app.url_for('second_route') == '/second'

def test_url_for_with_route_name_conflict(app):
    @app.route('/conflict', name='conflict')
    async def conflict_handler(request):
        return text('conflict response')

    @app.route('/conflict/another', name='conflict')
    async def another_conflict_handler(request):
        return text('another conflict response')

    assert app.url_for('conflict') == '/conflict'
    assert app.url_for('conflict') == '/conflict/another'  # This should raise an error or handle conflict

def test_url_for_with_dynamic_route(app):
    @app.route('/user/<user_id>', methods=['GET'], name='user_profile')
    async def user_profile(request, user_id):
        return text(f'User ID: {user_id}')

    assert app.url_for('user_profile', user_id=123) == '/user/123'