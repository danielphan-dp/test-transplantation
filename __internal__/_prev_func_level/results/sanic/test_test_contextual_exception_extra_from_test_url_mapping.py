import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('debug', (True, False))
def test_post_method_response(debug):
    app = Sanic("Test")

    @app.post("/post")
    async def post_method(request):
        return text('I am post method')

    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

    # Test with additional headers
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.post("/post", headers=headers)
    assert response.status == 200
    assert response.text == 'I am post method'

    # Test with invalid method
    request, response = app.test_client.get("/post")
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text

    # Test with empty body
    request, response = app.test_client.post("/post", data="")
    assert response.status == 200
    assert response.text == 'I am post method'