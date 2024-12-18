import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png'])
def test_get_method(app: Sanic, file_name: str):
    @app.route("/test", methods=["GET"])
    def test_route(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

    # Test with invalid headers
    request, response = app.test_client.get("/test", headers={"if-modified-since": "invalid-value"})
    assert response.status == 200
    assert response.text == 'I am get method'

    request, response = app.test_client.get("/test", headers={"if-modified-since": ""})
    assert response.status == 200
    assert response.text == 'I am get method'

    # Test with additional parameters
    request, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'