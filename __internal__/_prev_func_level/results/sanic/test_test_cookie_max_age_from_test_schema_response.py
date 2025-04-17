import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_data', [
    {'param': 'test'},
    {'param': ''},
    {'param': None},
])
def test_get_method(app, request_data):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", json=request_data)
    
    assert response.status == 200
    assert response.text == 'I am get method'