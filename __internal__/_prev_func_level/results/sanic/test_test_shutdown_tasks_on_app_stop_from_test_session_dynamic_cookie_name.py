import pytest
from sanic import Sanic
from sanic.response import text

class TestSanic(Sanic):
    pass

app = TestSanic("Test")

@app.route("/get")
def get_method(request):
    return text('I am get method')

@pytest.mark.asyncio
async def test_get_method():
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

@pytest.mark.asyncio
async def test_get_method_invalid_route():
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_params():
    request, response = app.test_client.get("/get?param=value")
    assert response.text == 'I am get method'
    assert response.status == 200

@pytest.mark.asyncio
async def test_get_method_with_headers():
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == 'I am get method'
    assert response.status == 200
    assert response.headers.get("Custom-Header") == "value"