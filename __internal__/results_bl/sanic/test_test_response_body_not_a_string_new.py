import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.filterwarnings('ignore:Types other than str will be')
def test_get_method_response(app):
    """Test the get method response"""
    
    @app.route("/get")
    async def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_response_not_a_string(app):
    """Test when the response body is not a string"""
    random_num = choice(range(1000))

    @app.route("/get_random")
    async def get_random_route(request):
        return text(random_num)

    request, response = app.test_client.get("/get_random")
    assert response.status == 500
    assert b"Internal Server Error" in response.body