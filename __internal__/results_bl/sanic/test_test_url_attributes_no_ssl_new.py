import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('path,query,expected_url', [
    ('/foo', '', 'http://{}:{}/foo'),
    ('/bar/baz', '', 'http://{}:{}/bar/baz'),
    ('/moo/boo', 'arg1=val1', 'http://{}:{}/moo/boo?arg1=val1'),
    ('/empty', '', 'http://{}:{}/empty'),
    ('/special/chars!@#$', '', 'http://{}:{}/special/chars!@#$'),
])
async def test_get_method(app, path, query, expected_url):
    @app.get(path)
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(path + f"?{query}")
    assert request.url == expected_url.format(HOST, request.server_port)

    parsed = urlparse(request.url)

    assert parsed.scheme == request.scheme
    assert parsed.path == request.path
    assert parsed.query == request.query_string
    assert parsed.netloc == request.host

@pytest.mark.parametrize('path', [
    ('/nonexistent'),
    ('/foo/bar/baz'),
])
async def test_get_method_not_found(app, path):
    @app.get(path)
    async def handler(request):
        return text('Not Found', status=404)

    request, response = app.test_client.get(path)
    assert response.status == 404
    assert response.text == 'Not Found'