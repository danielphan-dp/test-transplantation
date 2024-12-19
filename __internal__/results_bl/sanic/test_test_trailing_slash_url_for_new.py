import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("TestApp")

@app.route('/url-for')
def url_for(request):
    return text('url-for')

@pytest.mark.parametrize('path,strict,expected', [
    ('/url-for', False, '/url-for'),
    ('/url-for/', False, '/url-for'),
    ('/url-for', True, '/url-for'),
    ('/url-for/', True, '/url-for/'),
    ('/url-for/extra', False, '/url-for/extra'),
    ('/url-for/extra/', False, '/url-for/extra'),
    ('/url-for/extra', True, '/url-for/extra'),
    ('/url-for/extra/', True, '/url-for/extra/'),
])
def test_url_for(app, path, strict, expected):
    @app.route(path, strict_slashes=strict)
    def handler(*_):
        return text('handler')

    url = app.url_for("handler")
    assert url == expected

def test_url_for_invalid_route(app):
    with pytest.raises(Exception):
        app.url_for("non_existent_handler")