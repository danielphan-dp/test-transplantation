import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("test")

@app.route("/get", methods=["GET"])
def get(request):
    return text('I am get method')

def test_get_method_response():
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.content_type == "text/plain; charset=utf-8"

def test_get_method_invalid_route():
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param():
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.content_type == "text/plain; charset=utf-8"