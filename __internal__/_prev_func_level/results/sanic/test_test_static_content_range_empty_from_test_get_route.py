import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_path', ['/'])
def test_get_method(app, request_path):
    @app.get(request_path)
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'