import ssl
import pytest
from sanic import Sanic
from sanic.response import text
from urllib.parse import urlparse
from sanic_testing.testing import HOST, PORT

@pytest.mark.parametrize('path,query,expected_url', [
    ('/foo', '', 'https://{}:{}/foo'),
    ('/bar/baz', '', 'https://{}:{}/bar/baz'),
    ('/moo/boo', 'arg1=val1', 'https://{}:{}/moo/boo?arg1=val1'),
    ('/empty', '', 'https://{}:{}/empty'),
    ('/special_chars', 'arg1=val1&arg2=val2', 'https://{}:{}/special_chars?arg1=val1&arg2=val2'),
    ('/nonexistent', '', 'https://{}:{}/nonexistent')
])
async def test_get_method_with_ssl_context(app, path, query, expected_url):
    context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain('localhost_cert', 'localhost_key')

    @app.get(path)
    async def handler(request):
        return text('I am get method')

    request, _ = app.test_client.get(
        f"https://{HOST}:{PORT}" + path + f"?{query}",
        server_kwargs={"ssl": context},
    )
    
    assert request.url == expected_url.format(HOST, request.server_port)

    parsed = urlparse(request.url)

    assert parsed.scheme == request.scheme
    assert parsed.path == request.path
    assert parsed.query == request.query_string
    assert parsed.netloc == request.host

    response_text = await handler(request)
    assert response_text.body.decode() == 'I am get method'