import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_data', [
    {'method': 'GET', 'expected_status': 200, 'expected_body': 'I am get method'},
    {'method': 'POST', 'expected_status': 405, 'expected_body': 'Method POST not allowed for URL /'},
])
def test_get_method(app, request_data):
    @app.get("/")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/") if request_data['method'] == 'GET' else app.test_client.post("/")
    
    assert response.status == request_data['expected_status']
    if response.status == 200:
        assert response.text == request_data['expected_body']