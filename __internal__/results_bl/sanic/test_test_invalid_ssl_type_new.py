import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.get("/test")
async def handler(request):
    return text("I am get method")

def test_get_method_valid(app):
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_ssl(app):
    with pytest.raises(ValueError) as excinfo:
        app.test_client.get("/test", server_kwargs={"ssl": False})
    assert "Invalid ssl argument" in str(excinfo.value)

def test_get_method_no_ssl(app):
    request, response = app.test_client.get("/test", server_kwargs={"ssl": True})
    assert response.status == 200
    assert response.text == "I am get method"