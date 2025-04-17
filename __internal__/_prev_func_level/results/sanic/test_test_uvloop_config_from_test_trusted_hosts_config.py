import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url', ["/", "/test"])
def test_get_method(app: Sanic, url):
    @app.get(url)
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get(url)
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_not_found(app: Sanic):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param(app: Sanic):
    @app.get("/get_with_param")
    def handler(request):
        return text(f"Received param: {request.args.get('param', 'None')}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "Received param: test"
    assert response.status == 200

def test_get_method_with_empty_query_param(app: Sanic):
    @app.get("/get_with_empty_param")
    def handler(request):
        return text(f"Received param: {request.args.get('param', 'None')}")

    request, response = app.test_client.get("/get_with_empty_param?param=")
    assert response.text == "Received param: None"
    assert response.status == 200