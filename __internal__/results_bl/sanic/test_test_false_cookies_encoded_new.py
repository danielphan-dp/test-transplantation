import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_method,expected_response', [
    ('GET', 'I am get method'),
    ('POST', 'Method not allowed'),
])
def test_get_method(app, request_method, expected_response):
    @app.route("/", methods=['GET', 'POST'])
    def handler(request):
        if request.method == 'GET':
            return text('I am get method')
        return text('Method not allowed', status=405)

    request, response = app.test_client.request(request_method, "/")
    
    assert response.text == expected_response