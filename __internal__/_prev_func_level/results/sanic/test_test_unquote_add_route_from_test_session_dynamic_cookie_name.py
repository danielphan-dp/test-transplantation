import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('unquote', [True, False, None])
def test_get_method(app, unquote):
    @app.route('/get', methods=['GET'])
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get('/get')
    assert response.text == 'I am get method'

    # Test with unquoted URL
    if unquote:
        request, response = app.test_client.get('/get')
        assert response.text == 'I am get method'
    else:
        request, response = app.test_client.get('/get')
        assert response.text == 'I am get method'