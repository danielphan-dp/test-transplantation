import json
import pytest
from sanic import Sanic, Request, json as sanic_json
from ujson import loads as sloads

def test_post_method():
    app = Sanic("TestApp")

    @app.post("/post")
    def post_handler(request):
        return sanic_json({"message": "I am post method"})

    req, res = app.test_client.post("/post")
    assert res.status == 200
    assert sloads(res.body) == {"message": "I am post method"}

def test_post_method_with_data():
    app = Sanic("TestApp")

    @app.post("/post")
    def post_handler(request):
        return sanic_json({"received": request.json})

    req_body = {"key": "value"}
    req, res = app.test_client.post("/post", json=req_body)
    assert res.status == 200
    assert sloads(res.body) == {"received": req_body}

def test_post_method_empty_body():
    app = Sanic("TestApp")

    @app.post("/post")
    def post_handler(request):
        return sanic_json({"error": "No data provided"} if not request.json else {"message": "Data received"})

    req, res = app.test_client.post("/post", json={})
    assert res.status == 200
    assert sloads(res.body) == {"error": "No data provided"}

def test_post_method_invalid_json():
    app = Sanic("TestApp")

    @app.post("/post")
    def post_handler(request):
        return sanic_json({"error": "Invalid JSON"}, status=400)

    req, res = app.test_client.post("/post", data="invalid json")
    assert res.status == 400
    assert sloads(res.body) == {"error": "Invalid JSON"}