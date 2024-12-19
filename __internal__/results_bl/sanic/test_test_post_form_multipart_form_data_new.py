import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('payload', [
    '------sanic\r\nContent-Disposition: form-data; name="test"\r\n\r\nOK\r\n------sanic--\r\n',
    '------sanic\r\ncontent-disposition: form-data; name="test"\r\n\r\nOK\r\n------sanic--\r\n',
    '------sanic\r\nContent-Disposition: form-data; name="test"\r\n\r\n\r\n------sanic--\r\n',  # Edge case: empty value
    '------sanic\r\nContent-Disposition: form-data; name="test"\r\n\r\nInvalid\r\n------sanic--\r\n'  # Edge case: different value
])
def test_get_method(app, payload):
    @app.route("/", methods=["GET"])
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/")
    
    assert response.text == 'I am get method'  # Test the GET method response
    assert request.method == 'GET'  # Ensure the method is GET
    assert response.status == 200  # Check for successful response status