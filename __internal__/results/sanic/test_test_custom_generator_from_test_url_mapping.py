import pytest
from sanic import Sanic, response
from sanic.request import Request

app = Sanic("test_app")

@app.get("/test")
async def get_method(request: Request):
    return response.text('I am get method')

def test_get_method_success():
    request, response = app.test_client.get("/test")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_invalid_route():
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_headers():
    request, response = app.test_client.get("/test", headers={"Custom-Header": "value"})
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_query_params():
    request, response = app.test_client.get("/test?param=value")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_empty_response():
    @app.get("/empty")
    async def empty_response(request: Request):
        return response.text('')

    request, response = app.test_client.get("/empty")
    assert response.text == ''
    assert response.status == 200

def test_get_method_405_method_not_allowed():
    request, response = app.test_client.post("/test")
    assert response.status == 405
    assert "Method POST not allowed for URL /test" in response.text