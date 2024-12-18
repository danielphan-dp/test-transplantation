import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or platform.system() == 'Windows', reason='Not testable with current client')
def test_get_method_response(app):
    @app.get("/test-get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test-get")
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_context(app):
    class DummyView:
        def get(self, request):
            return text('I am get method with context')

    app.add_route(DummyView().get, "/context")

    request, response = app.test_client.get("/context")
    
    assert response.status == 200
    assert response.text == 'I am get method with context'

def test_get_method_with_query_params(app):
    @app.get("/test-get-query")
    async def get_with_query(request):
        name = request.args.get('name', 'World')
        return text(f'Hello, {name}!')

    request, response = app.test_client.get("/test-get-query?name=Test")
    
    assert response.status == 200
    assert response.text == 'Hello, Test!'

def test_get_method_no_query_params(app):
    @app.get("/test-get-query")
    async def get_with_query(request):
        return text('Hello, World!')

    request, response = app.test_client.get("/test-get-query")
    
    assert response.status == 200
    assert response.text == 'Hello, World!'