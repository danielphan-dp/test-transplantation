import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_method', ['GET', 'POST', 'PUT', 'DELETE'])
def test_get_method_response(app: Sanic, request_method: str):
    @app.route("/test", methods=["GET", "POST", "PUT", "DELETE"])
    def test_route(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    assert response.text == 'I am get method'
    assert response.status == 200

    if request_method == 'POST':
        request, response = app.test_client.post("/test")
        assert response.text == 'I am get method'
        assert response.status == 200

    if request_method == 'PUT':
        request, response = app.test_client.put("/test")
        assert response.text == 'I am get method'
        assert response.status == 200

    if request_method == 'DELETE':
        request, response = app.test_client.delete("/test")
        assert response.text == 'I am get method'
        assert response.status == 200

def test_get_method_invalid_route(app: Sanic):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_no_route(app: Sanic):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text