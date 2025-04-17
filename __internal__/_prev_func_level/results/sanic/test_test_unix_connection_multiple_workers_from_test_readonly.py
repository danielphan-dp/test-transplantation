import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_get_method_response():
    app = Sanic(name="test")
    
    @app.get("/")
    async def handler(request: Request):
        return text("I am get method")
    
    request, response = app.test_client.get("/")
    
    assert response.status == 200, f"Expected status 200, got {response.status}"
    assert response.text == "I am get method", f"Expected response text 'I am get method', got {response.text}"

def test_get_method_with_query_param():
    app = Sanic(name="test")
    
    @app.get("/greet")
    async def greet_handler(request: Request):
        name = request.args.get('name', 'Guest')
        return text(f"I am get method, hello {name}")
    
    request, response = app.test_client.get("/greet?name=John")
    
    assert response.status == 200, f"Expected status 200, got {response.status}"
    assert response.text == "I am get method, hello John", f"Expected response text 'I am get method, hello John', got {response.text}"

def test_get_method_with_no_query_param():
    app = Sanic(name="test")
    
    @app.get("/greet")
    async def greet_handler(request: Request):
        name = request.args.get('name', 'Guest')
        return text(f"I am get method, hello {name}")
    
    request, response = app.test_client.get("/greet")
    
    assert response.status == 200, f"Expected status 200, got {response.status}"
    assert response.text == "I am get method, hello Guest", f"Expected response text 'I am get method, hello Guest', got {response.text}"