import pytest
from sanic import Sanic
from sanic.response import text
from urllib.parse import urlparse

@pytest.mark.parametrize('path,query,expected_url', [
    ('/foo', '', 'https://{}:{}/foo'),
    ('/bar/baz', '', 'https://{}:{}/bar/baz'),
    ('/moo/boo', 'arg1=val1', 'https://{}:{}/moo/boo?arg1=val1'),
    ('/empty', '', 'https://{}:{}/empty'),
    ('/special/chars?query=1&other=2', '', 'https://{}:{}/special/chars?query=1&other=2'),
    ('/path/with/space%20in%20it', '', 'https://{}:{}/path/with/space%20in%20it'),
])
async def test_get_method_with_ssl_dict(app, path, query, expected_url):
    ssl_dict = {"cert": localhost_cert, "key": localhost_key}

    @app.get(path)
    async def handler(request):
        return text('I am get method')

    request, _ = app.test_client.get(
        f"https://{HOST}:{PORT}" + path + f"?{query}",
        server_kwargs={"ssl": ssl_dict},
    )
    
    assert request.url == expected_url.format(HOST, request.server_port)

    parsed = urlparse(request.url)

    assert parsed.scheme == request.scheme
    assert parsed.path == request.path
    assert parsed.query == request.query_string
    assert parsed.netloc == request.host

    # Additional assertions for edge cases
    if path == '/empty':
        assert request.text == 'I am get method'
    elif path == '/special/chars?query=1&other=2':
        assert request.text == 'I am get method'
    elif path == '/path/with/space%20in%20it':
        assert request.text == 'I am get method'