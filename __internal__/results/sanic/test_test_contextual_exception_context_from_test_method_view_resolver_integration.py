import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('debug', (True, False))
def test_post_method(debug):
    app = Sanic("Test")

    @app.post("/test")
    async def post_method(request):
        return text('I am post method')

    request, response = app.test_client.post("/test", debug=debug)
    assert response.status == 200
    assert response.text == 'I am post method'

    # Test with additional headers
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.post("/test", headers=headers, debug=debug)
    assert response.status == 200
    assert response.text == 'I am post method'

    # Test with empty body
    request, response = app.test_client.post("/test", data='', debug=debug)
    assert response.status == 200
    assert response.text == 'I am post method'

    # Test with invalid route
    request, response = app.test_client.post("/invalid_route", debug=debug)
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

    # Test with method not allowed
    request, response = app.test_client.get("/test", debug=debug)
    assert response.status == 405
    assert "Method GET not allowed for URL /test" in response.text