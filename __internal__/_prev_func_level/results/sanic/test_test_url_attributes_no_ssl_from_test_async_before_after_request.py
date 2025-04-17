import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('path, expected_response', [
    ('/get', 'I am get method'),
    ('/nonexistent', 'Not Found'),
])
def test_get_method(app, path, expected_response):
    @app.get('/get')
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(path)
    
    if path == '/get':
        assert response.text == expected_response
        assert response.status == 200
    else:
        assert response.status == 404
        assert "Not Found" in response.text

    parsed = urlparse(request.url)
    assert parsed.path == request.path
    assert parsed.netloc == request.host
    assert parsed.scheme == request.scheme