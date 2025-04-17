import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_method', ['GET', 'POST'])
def test_get_method_response(app: Sanic, request_method: str):
    @app.route("/test_get", methods=[request_method])
    def test_get_route(request):
        return text('I am get method')

    request, response = app.test_client.get("/test_get") if request_method == 'GET' else app.test_client.post("/test_get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_request(app: Sanic):
    @app.route("/test_get_invalid", methods=["GET"])
    def test_get_invalid_route(request):
        return text('I am get method')

    request, response = app.test_client.get("/test_get_invalid", headers={"invalid-header": "invalid-value"})
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_empty_request(app: Sanic):
    @app.route("/test_get_empty", methods=["GET"])
    def test_get_empty_route(request):
        return text('I am get method')

    request, response = app.test_client.get("/test_get_empty", headers={})
    assert response.status == 200
    assert response.text == 'I am get method'