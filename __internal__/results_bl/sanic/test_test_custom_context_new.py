import random
from sanic.response import text
from sanic.response import json
from ujson import loads

def test_get_method(app):
    @app.route("/get")
    def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_custom_context(app):
    @app.middleware("request")
    def store(request):
        request.ctx.user = "sanic"
        request.ctx.session = None

    @app.route("/get_with_context")
    def get_with_context_handler(request):
        return json({
            "user": request.ctx.user,
            "session": request.ctx.session,
            "has_user": hasattr(request.ctx, "user"),
            "has_session": hasattr(request.ctx, "session"),
        })

    request, response = app.test_client.get("/get_with_context")
    assert response.json == {
        "user": "sanic",
        "session": None,
        "has_user": True,
        "has_session": True,
    }

def test_get_method_with_missing_context(app):
    @app.route("/get_missing_context")
    def get_missing_context_handler(request):
        try:
            invalid = request.ctx.missing
        except AttributeError as e:
            invalid = str(e)
        return json({"invalid": invalid})

    request, response = app.test_client.get("/get_missing_context")
    assert response.json == {
        "invalid": "'types.SimpleNamespace' object has no attribute 'missing'"
    }