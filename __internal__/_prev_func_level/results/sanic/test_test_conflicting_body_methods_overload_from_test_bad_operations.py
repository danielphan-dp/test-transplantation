import pytest
from sanic import Sanic
from sanic.response import text, json

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.put("/put_test")
    async def put_test(request):
        return text('I am put method')

    return app

def test_put_method(app):
    payload = {"test": "OK"}
    
    request, response = app.test_client.put("/put_test", json=payload)
    assert response.status == 200
    assert response.text == 'I am put method'

def test_put_method_with_empty_body(app):
    request, response = app.test_client.put("/put_test", json={})
    assert response.status == 200
    assert response.text == 'I am put method'

def test_put_method_with_invalid_json(app):
    request, response = app.test_client.put("/put_test", data="invalid json")
    assert response.status == 200
    assert response.text == 'I am put method'

def test_put_method_with_large_payload(app):
    large_payload = {"data": "x" * 10000}
    request, response = app.test_client.put("/put_test", json=large_payload)
    assert response.status == 200
    assert response.text == 'I am put method'