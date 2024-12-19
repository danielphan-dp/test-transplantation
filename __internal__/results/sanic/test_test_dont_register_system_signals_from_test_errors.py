import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.skipif(os.name == 'nt', reason='May hang CI on py38/windows')
def test_get_method(app):
    @app.route("/get")
    async def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers.get("content-type") == "text/plain; charset=utf-8"

def test_get_method_with_query_param(app):
    @app.route("/get")
    async def get_route(request):
        name = request.args.get('name', 'World')
        return text(f'I am get method, {name}')

    request, response = app.test_client.get("/get?name=Tester")
    
    assert response.status == 200
    assert response.text == "I am get method, Tester"

def test_get_method_with_no_route(app):
    request, response = app.test_client.get("/nonexistent")
    
    assert response.status == 404
    assert response.headers.get("content-type") == "application/problem+json"
    error_response = response.json()
    assert error_response["type"] == "about:blank"
    assert error_response["title"] == "Not Found"
    assert error_response["status"] == 404

def test_get_method_with_invalid_method(app):
    @app.route("/get", methods=["POST"])
    async def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    
    assert response.status == 405
    assert response.headers.get("content-type") == "application/problem+json"
    error_response = response.json()
    assert error_response["type"] == "about:blank"
    assert error_response["title"] == "Method Not Allowed"
    assert error_response["status"] == 405