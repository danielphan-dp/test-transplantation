import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("TestApp")

@app.route('/url-for')
def url_for(request):
    return text('url-for')

@pytest.mark.parametrize('path,version,expected', [
    ('/url-for', 1, '/v1/url-for'),
    ('/url-for', 1.1, '/v1.1/url-for'),
    ('/url-for', '1', '/v1/url-for'),
    ('/url-for', '1.1', '/v1.1/url-for'),
    ('/url-for', '1.0.1', '/v1.0.1/url-for'),
    ('/url-for', 'v1.0.1', '/v1.0.1/url-for'),
    ('/url-for', 0, '/v0/url-for'),
    ('/url-for', -1, '/v-1/url-for'),
    ('/url-for', None, '/url-for'),
])
def test_url_for_versioning(app, path, version, expected):
    @app.route(path, version=version)
    def handler(*_):
        return text('handler')

    url = app.url_for("handler")
    assert url == expected

def test_url_for_no_version(app):
    url = app.url_for("url_for")
    assert url == '/url-for'