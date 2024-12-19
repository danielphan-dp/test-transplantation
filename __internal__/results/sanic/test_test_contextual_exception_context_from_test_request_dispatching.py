import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('debug', (True, False))
def test_post_method_response(debug):
    app = Sanic("Test")

    @app.post("/post")
    def post_method(request):
        return text('I am post method')

    request, response = app.test_client.post("/post", debug=debug)
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_invalid_route(debug):
    app = Sanic("Test")

    @app.post("/post")
    def post_method(request):
        return text('I am post method')

    request, response = app.test_client.get("/post", debug=debug)
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text

def test_post_method_with_data(debug):
    app = Sanic("Test")

    @app.post("/post")
    def post_method(request):
        return text(f'Received data: {request.json}')

    request, response = app.test_client.post("/post", json={"key": "value"}, debug=debug)
    assert response.status == 200
    assert response.text == 'Received data: {"key": "value"}'