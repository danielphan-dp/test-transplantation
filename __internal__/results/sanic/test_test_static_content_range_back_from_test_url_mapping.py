import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_method_response(file_name):
    app = Sanic("test_app")

    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

    # Test with invalid method
    request, response = app.test_client.post("/test")
    assert response.status == 405
    assert "Method POST not allowed for URL /test" in response.text

    # Test with additional headers
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/test", headers=headers)
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers["Custom-Header"] != "value"  # Ensure custom header is not in response

    # Test with query parameters
    request, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure query params do not affect response

    # Test with a non-existent route
    request, response = app.test_client.get("/non_existent")
    assert response.status == 404
    assert "Requested URL /non_existent not found" in response.text