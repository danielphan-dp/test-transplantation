import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_method', ['GET', 'POST'])
def test_get_method_response(app, request_method):
    @app.route('/get', methods=[request_method])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get('/get') if request_method == 'GET' else app.test_client.post('/get')
    
    assert response.status == 200
    assert response.text == 'I am get method'