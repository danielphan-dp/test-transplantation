import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/put", methods=["PUT"])
    async def put_method(request):
        return text("I am put method")

    return app

def test_put_method(app):
    request, response = app.test_client.put("/put")
    assert response.text == "I am put method"
    assert response.status == 200

def test_put_method_with_invalid_data(app):
    request, response = app.test_client.put("/put", data="invalid data")
    assert response.text == "I am put method"
    assert response.status == 200

def test_put_method_not_found(app):
    request, response = app.test_client.put("/nonexistent")
    assert response.status == 404

def test_put_method_with_headers(app):
    request, response = app.test_client.put("/put", headers={"Custom-Header": "value"})
    assert response.text == "I am put method"
    assert response.status == 200

def test_put_method_with_empty_body(app):
    request, response = app.test_client.put("/put", data="")
    assert response.text == "I am put method"
    assert response.status == 200

def test_put_method_with_large_body(app):
    large_data = "x" * 10000
    request, response = app.test_client.put("/put", data=large_data)
    assert response.text == "I am put method"
    assert response.status == 200