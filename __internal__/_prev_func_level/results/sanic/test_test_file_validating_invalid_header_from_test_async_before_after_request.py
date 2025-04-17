import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_method', ['GET', 'POST', 'PUT', 'DELETE'])
def test_get_method_with_different_http_methods(app: Sanic, request_method: str):
    @app.route("/get", methods=["GET", "POST", "PUT", "DELETE"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get") if request_method == 'GET' else app.test_client.post("/get") if request_method == 'POST' else app.test_client.put("/get") if request_method == 'PUT' else app.test_client.delete("/get")
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app: Sanic):
    request, response = app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_with_custom_header(app: Sanic):
    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'