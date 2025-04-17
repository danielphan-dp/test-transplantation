import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_data', [
    {'method': 'GET', 'url': '/get', 'expected': 'I am get method'},
    {'method': 'POST', 'url': '/get', 'expected_status': 405},
    {'method': 'PUT', 'url': '/get', 'expected_status': 405},
    {'method': 'DELETE', 'url': '/get', 'expected_status': 405},
])
def test_get_method(app, request_data):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, request_data['url'], methods=['GET'])
    
    if request_data['method'] == 'GET':
        request, response = app.test_client.get(request_data['url'])
        assert response.text == request_data['expected']
    else:
        request, response = app.test_client.get(request_data['url'], method=request_data['method'])
        assert response.status == request_data['expected_status']