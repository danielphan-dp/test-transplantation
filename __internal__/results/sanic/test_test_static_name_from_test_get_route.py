import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url', ['/'])
def test_get_method(app, url):
    @app.get(url)
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(url)

    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('url', ['/nonexistent'])
def test_get_method_not_found(app, url):
    request, response = app.test_client.get(url)

    assert response.status == 404
    assert "Requested URL" in response.text

@pytest.mark.parametrize('url', ['/'])
def test_get_method_with_query_params(app, url):
    @app.get(url)
    async def handler(request):
        return text(f'I am get method with query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get(f'{url}?param=test')

    assert response.status == 200
    assert response.text == 'I am get method with query param: test'