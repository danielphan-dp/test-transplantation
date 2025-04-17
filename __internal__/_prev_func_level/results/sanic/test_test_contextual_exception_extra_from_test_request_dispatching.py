import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import SanicException

@pytest.mark.parametrize('debug', (True, False))
def test_post_method_response(debug):
    app = Sanic("Test")

    @app.post("/post")
    def post_method(request):
        return text('I am post method')

    request, response = app.test_client.post("/post", debug=debug)
    assert response.status == 200
    assert response.text == 'I am post method'

    # Testing with invalid method
    request, response = app.test_client.get("/post", debug=debug)
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text

    # Testing with additional headers
    request, response = app.test_client.post("/post", headers={"X-Custom-Header": "value"}, debug=debug)
    assert response.status == 200
    assert response.text == 'I am post method'