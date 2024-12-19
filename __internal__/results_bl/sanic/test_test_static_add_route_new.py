import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('strict_slashes', [True, False, None])
def test_get_method(app, strict_slashes):
    @app.get('/get')
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get('/get')
    assert response.text == 'I am get method'

    request, response = app.test_client.get('/get/')
    if strict_slashes is True:
        assert response.status == 404
    else:
        assert response.text == 'I am get method' if strict_slashes is False else response.status == 404

    request, response = app.test_client.get('/nonexistent')
    assert response.status == 404