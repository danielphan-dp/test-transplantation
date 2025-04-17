import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_method', ['GET', 'POST'])
def test_get_method_response(request_method):
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/") if request_method == 'GET' else app.test_client.post("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found():
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param():
    app = Sanic("test_app")

    @app.get("/query")
    def get_method(request):
        return text(f'I am get method with query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/query?param=test")
    assert response.status == 200
    assert response.text == 'I am get method with query param: test'