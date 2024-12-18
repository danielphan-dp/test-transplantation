import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.mark.parametrize('path,version,expected', [
    ('/url-for', 1, '/v1/url-for'),
    ('/url-for', 1.1, '/v1.1/url-for'),
    ('/url-for', '1', '/v1/url-for'),
    ('/url-for', '1.1', '/v1.1/url-for'),
    ('/url-for', '1.0.1', '/v1.0.1/url-for'),
    ('/url-for', 'v1.0.1', '/v1.0.1/url-for'),
])
def test_url_for_with_versioning(app, path, version, expected):
    @app.route(path, version=version)
    def handler(request):
        return text('url-for')

    url = app.url_for("handler")
    assert url == expected

def test_fails_if_endpoint_not_found(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_handler")
        e.match("Endpoint with name `app.non_existent_handler` was not found")