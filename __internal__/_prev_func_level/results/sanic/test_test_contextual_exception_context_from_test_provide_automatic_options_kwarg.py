import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('debug', (True, False))
def test_post_method_response(debug):
    app = Sanic("Test")

    @app.post("/post")
    async def post_method(request):
        return text('I am post method')

    request, response = app.test_client.post("/post", debug=debug)
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_invalid_route(debug):
    app = Sanic("Test")

    request, response = app.test_client.post("/invalid_route", debug=debug)
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_post_method_with_data(debug):
    app = Sanic("Test")

    @app.post("/post/data")
    async def post_with_data(request):
        data = request.json
        return text(f"Received: {data}")

    request, response = app.test_client.post("/post/data", json={"key": "value"}, debug=debug)
    assert response.status == 200
    assert response.text == 'Received: {"key": "value"}'