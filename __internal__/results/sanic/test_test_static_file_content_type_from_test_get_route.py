import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('url', ['/'])
def test_get_method_response(app, url):
    @app.get(url)
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(url)
    
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'