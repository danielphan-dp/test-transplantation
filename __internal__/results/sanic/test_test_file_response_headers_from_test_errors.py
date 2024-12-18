import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_data', [
    {'name': 'test'},
    {'name': 'get'},
    {},
])
def test_get_method(app: Sanic, request_data):
    @app.route("/get", methods=["GET"])
    def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", json=request_data)
    
    assert response.status == 200
    assert response.text == 'I am get method'

    if request_data:
        assert 'name' in request_data
    else:
        assert response.text == 'I am get method'