import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize("expected", ["I am get method"])
def test_get_method_response(app: Sanic, expected):
    @app.get("/")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == expected

def test_get_method_response_with_different_content(app: Sanic):
    @app.get("/")
    def handler(request):
        return text("Different response")

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == "Different response"

def test_get_method_response_with_empty_body(app: Sanic):
    @app.get("/")
    def handler(request):
        return text("")

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == ""