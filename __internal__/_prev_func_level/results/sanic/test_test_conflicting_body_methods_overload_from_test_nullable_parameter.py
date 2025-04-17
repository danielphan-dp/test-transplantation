import pytest
from sanic import Sanic
from sanic.response import text, json

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.put("/put_test")
    async def put_test(request):
        return text('I am put method')

    return app

def test_put_method(app):
    payload = {"test": "OK"}
    
    # Test basic PUT request
    request, response = app.test_client.put("/put_test", json=payload)
    assert response.status == 200
    assert response.text == 'I am put method'

    # Test PUT request with empty body
    request, response = app.test_client.put("/put_test", json={})
    assert response.status == 200
    assert response.text == 'I am put method'

    # Test PUT request with invalid data type
    request, response = app.test_client.put("/put_test", data="invalid_data")
    assert response.status == 200
    assert response.text == 'I am put method'

    # Test PUT request with missing endpoint
    request, response = app.test_client.put("/non_existent_endpoint", json=payload)
    assert response.status == 404  # Assuming the app returns 404 for non-existent endpoints

    # Test PUT request with malformed JSON
    request, response = app.test_client.put("/put_test", data="{'test': 'malformed_json'}", headers={"Content-Type": "application/json"})
    assert response.status == 200
    assert response.text == 'I am put method'