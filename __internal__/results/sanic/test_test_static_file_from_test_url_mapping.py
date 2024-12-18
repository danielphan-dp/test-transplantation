import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_method', ['GET', 'POST', 'PUT', 'DELETE'])
def test_get_method_response(request_method):
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text('I am get method')

    app.router.finalize()

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

    request, response = app.test_client.post("/")
    assert response.status == 405  # Method not allowed

    request, response = app.test_client.put("/")
    assert response.status == 405  # Method not allowed

    request, response = app.test_client.delete("/")
    assert response.status == 405  # Method not allowed

    # Test with invalid URL
    request, response = app.test_client.get("/invalid")
    assert response.status == 404  # Not found

    # Test with additional headers
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"