import pytest
from sanic import Sanic, Request, json, text

def test_post_method_response():
    app = Sanic("TestApp")

    @app.post("/post")
    def post_handler(request):
        return text('I am post method')

    request, response = app.test_client.post("/post")
    assert response.text == 'I am post method'
    assert response.status == 200

def test_post_method_with_data():
    app = Sanic("TestApp")

    @app.post("/post")
    def post_handler(request):
        return json({"received": request.json})

    req_body = {"key": "value"}
    request, response = app.test_client.post("/post", json=req_body)
    assert response.json == {"received": req_body}
    assert response.status == 200

def test_post_method_empty_body():
    app = Sanic("TestApp")

    @app.post("/post")
    def post_handler(request):
        return json({"received": request.json})

    request, response = app.test_client.post("/post", json={})
    assert response.json == {"received": {}}
    assert response.status == 200

def test_post_method_invalid_json():
    app = Sanic("TestApp")

    @app.post("/post")
    def post_handler(request):
        return text('Invalid JSON', status=400)

    request, response = app.test_client.post("/post", data="invalid json")
    assert response.status == 400
    assert response.text == 'Invalid JSON'