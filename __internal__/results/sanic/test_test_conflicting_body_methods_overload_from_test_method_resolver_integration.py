import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.put("/test_put")
async def test_put(request):
    return text("I am put method")

def test_put_method(app):
    client = app.test_client()
    
    # Test valid PUT request
    request, response = client.put("/test_put")
    assert response.status == 200
    assert response.text == "I am put method"
    
    # Test PUT request with body
    request, response = client.put("/test_put", json={"key": "value"})
    assert response.status == 200
    assert response.text == "I am put method"
    
    # Test PUT request with invalid URL
    request, response = client.put("/invalid_url")
    assert response.status == 404  # Assuming the app returns 404 for invalid routes

    # Test PUT request with empty body
    request, response = client.put("/test_put", json={})
    assert response.status == 200
    assert response.text == "I am put method"