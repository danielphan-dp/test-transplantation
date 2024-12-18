import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('expected', [
    "I am get method",
])
def test_get_method_response(app: Sanic, expected):
    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    
    assert response.text == expected
    assert response.status == 200

def test_get_method_response_with_different_path(app: Sanic):
    @app.get("/another_get")
    def another_get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/another_get")
    
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_response_with_invalid_path(app: Sanic):
    request, response = app.test_client.get("/invalid_path")
    
    assert response.status == 404
    assert "Requested URL /invalid_path not found" in response.text