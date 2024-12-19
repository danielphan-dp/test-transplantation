import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.constants import HTTP_METHODS
from sanic.exceptions import URLBuildError
from sanic.response import text

@pytest.mark.parametrize('method', HTTP_METHODS)
def test_url_for_method(method):
    app = Sanic("app")
    
    @app.route('/url-for', methods=[method])
    def url_for_handler(request):
        return text('url-for')

    assert app.url_for('url_for_handler') == '/url-for'

    with pytest.raises(URLBuildError):
        app.url_for('non_existent_route')

    @app.route('/url-for/<param>', methods=[method])
    def url_for_with_param(request, param):
        return text(f'url-for with param: {param}')

    assert app.url_for('url_for_with_param', param='test') == '/url-for/test'