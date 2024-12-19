import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('max_age', [0, -1, None])
def test_get_method_with_edge_cases(app, max_age):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('max_age', [30.0, 30.1, 'test'])
def test_get_method_with_cookies(app, max_age):
    cookies = {"test": "wait"}

    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", cookies=cookies, raw_cookies=True)
    assert response.status == 200
    assert response.text == 'I am get method'