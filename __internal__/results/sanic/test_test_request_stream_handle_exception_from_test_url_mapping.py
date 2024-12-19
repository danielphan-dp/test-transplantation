import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_post_method(app):
    @app.post("/post")
    async def post(request):
        return text('I am post method')

    # Test valid POST request
    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

    # Test invalid method (GET)
    request, response = app.test_client.get("/post")
    assert response.status == 405
    assert "Method GET not allowed for URL /post" in response.text

    # Test invalid URL
    request, response = app.test_client.post("/invalid_post")
    assert response.status == 404
    assert "Requested URL /invalid_post not found" in response.text

    # Test POST with data
    request, response = app.test_client.post("/post", data={"key": "value"})
    assert response.status == 200
    assert response.text == 'I am post method'  # Ensure the response remains the same regardless of data

    # Test POST with empty body
    request, response = app.test_client.post("/post", data="")
    assert response.status == 200
    assert response.text == 'I am post method'  # Ensure the response remains the same with empty body