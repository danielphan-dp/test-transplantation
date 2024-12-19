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
    ('/invalid_path', '', 'https://{}:{}/invalid_path'),
])
def test_get_method_with_ssl_context(app, path, query, expected_url):
    context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(localhost_cert, localhost_key)

    @app.get(path)
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(
        f"https://{HOST}:{PORT}" + path + f"?{query}",
        server_kwargs={"ssl": context},
    )

    assert response.text == 'I am get method'
    assert request.url == expected_url.format(HOST, request.server_port)

    parsed = urlparse(request.url)

    assert parsed.scheme == request.scheme
    assert parsed.path == request.path
    assert parsed.query == request.query_string
    assert parsed.netloc == request.host

    if path == '/invalid_path':
        assert response.status == 404
    else:
        assert response.status == 200