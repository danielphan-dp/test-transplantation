import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.xfail
def test_get_method(app):
    """Test the GET method of the Sanic application."""
    
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    response = await app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.xfail
def test_get_method_with_invalid_route(app):
    """Test the GET method with an invalid route."""
    
    response = await app.test_client.get("/invalid")
    assert response.status == 404

@pytest.mark.xfail
def test_get_method_with_query_params(app):
    """Test the GET method with query parameters."""
    
    @app.get("/get_with_params")
    async def handler(request):
        return text(f"Received params: {request.args}")

    response = await app.test_client.get("/get_with_params?param1=value1&param2=value2")
    assert response.status == 200
    assert response.text == "Received params: MultiDict([('param1', ['value1']), ('param2', ['value2'])])"