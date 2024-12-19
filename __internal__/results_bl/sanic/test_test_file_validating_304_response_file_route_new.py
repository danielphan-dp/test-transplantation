import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_method', ['GET', 'POST'])
def test_get_method_response(app: Sanic, request_method: str):
    @app.route("/test", methods=[request_method])
    def test_route(request):
        return text('I am get method')

    _, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.body == b'I am get method'

    _, response = app.test_client.post("/test")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_invalid_route(app: Sanic):
    _, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_headers(app: Sanic):
    @app.route("/test_with_headers", methods=["GET"])
    def test_route(request):
        return text('I am get method')

    _, response = app.test_client.get("/test_with_headers", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.body == b'I am get method'