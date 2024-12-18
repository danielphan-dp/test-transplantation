import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route('/url-for', name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    return app

def test_url_for_existing_route(app):
    assert app.url_for('url_for_route') == '/url-for'

def test_url_for_with_params(app):
    @app.route('/<name>', name='greet')
    async def greet(request, name):
        return text(f'Hello, {name}!')

    assert app.url_for('greet', name='Alice') == '/Alice'

def test_url_for_nonexistent_route(app):
    with pytest.raises(URLBuildError):
        app.url_for('nonexistent_route')

def test_url_for_with_invalid_params(app):
    @app.route('/<int:id>', name='item')
    async def item(request, id):
        return text(f'Item {id}')

    with pytest.raises(URLBuildError):
        app.url_for('item')  # Missing required parameter 'id'

def test_url_for_with_server_name(app):
    app.config.update({"SERVER_NAME": "example.com"})
    assert app.url_for('url_for_route', _external=True) == 'http://example.com/url-for'