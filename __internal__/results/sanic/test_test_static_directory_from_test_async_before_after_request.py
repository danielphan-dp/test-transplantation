import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
@pytest.mark.parametrize('base_uri', ['/static', '', '/dir'])
def test_get_method(base_uri):
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

    # Test with different base_uri
    request, response = app.test_client.get(base_uri + "/get")
    assert response.status == 404  # Expecting 404 since the route does not exist at this base_uri

    # Test with invalid method
    request, response = app.test_client.post("/get")
    assert response.status == 405  # Expecting 405 Method Not Allowed

    # Test with additional parameters
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure the response remains the same with query parameters

    # Test with a non-existent route
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404  # Expecting 404 for non-existent route