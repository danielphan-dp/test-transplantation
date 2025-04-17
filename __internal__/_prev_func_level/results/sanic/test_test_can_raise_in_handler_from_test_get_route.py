import asyncio
from sanic import Sanic, Request, json
from sanic.response import text

app = Sanic("test_app")

@app.get("/")
async def handler(request: Request):
    return text('I am get method')

def test_get_method(app: Sanic):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app: Sanic):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app: Sanic):
    @app.get("/greet")
    async def greet_handler(request: Request):
        name = request.args.get('name', 'World')
        return text(f'Hello, {name}!')

    request, response = app.test_client.get("/greet?name=Alice")
    assert response.status == 200
    assert response.text == 'Hello, Alice!'

def test_get_method_with_empty_query_param(app: Sanic):
    @app.get("/greet")
    async def greet_handler(request: Request):
        name = request.args.get('name', 'World')
        return text(f'Hello, {name}!')

    request, response = app.test_client.get("/greet?name=")
    assert response.status == 200
    assert response.text == 'Hello, !'