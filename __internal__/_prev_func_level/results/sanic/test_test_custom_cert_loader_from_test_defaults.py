import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

app = Sanic("test_app")

@app.get("/get_method")
async def get_method(request):
    return text('I am get method')

@pytest.fixture
def client():
    return SanicTestClient(app)

def test_get_method(client):
    request, response = client.get("/get_method")
    assert response.status_code == 200
    assert response.text == 'I am get method'
    assert request.method == 'GET'
    assert request.path == '/get_method'

def test_get_method_not_found(client):
    request, response = client.get("/non_existent")
    assert response.status_code == 404

def test_get_method_with_query_params(client):
    request, response = client.get("/get_method?param=value")
    assert response.status_code == 200
    assert response.text == 'I am get method'
    assert request.args.get('param') == ['value']