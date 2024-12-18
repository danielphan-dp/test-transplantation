import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_method(file_name, static_file_directory):
    app = Sanic("test_app")

    @app.get("/get")
    def get(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

    # Test with additional parameters
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'

    # Test with invalid method
    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text

    # Test with non-existent route
    request, response = app.test_client.get("/non_existent")
    assert response.status == 404
    assert "Requested URL /non_existent not found" in response.text