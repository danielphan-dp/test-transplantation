import asyncio
import pytest
from sanic import Sanic
from sanic.exceptions import URLBuildError
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_valid_route(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    request, response = app.test_client.get('/url-for')
    assert response.text == 'url-for'
    assert app.url_for('url_for') == '/url-for'

def test_url_for_invalid_route(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

def test_url_for_with_dynamic_route(app):
    results = []

    async def handler(request, name):
        results.append(name)
        return text("OK")

    app.add_route(handler, "/folder/<name>", name="route_dynamic")
    assert app.url_for("route_dynamic", name="test") == "/folder/test"

def test_url_for_with_missing_parameter(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    with pytest.raises(TypeError):
        app.url_for('url_for')  # Missing required parameters if any are added later

def test_url_for_with_extra_parameters(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    assert app.url_for('url_for', extra_param='value') == '/url-for'  # Should ignore extra parameters