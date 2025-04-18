# This test file was generated from tests/test_basic.py to test src/flask/ctx.py through test transplantation.

import pytest
from flask import Flask, g, request, has_request_context, has_app_context, after_this_request, copy_current_request_context
from flask.ctx import _AppCtxGlobals, AppContext, RequestContext
from werkzeug.exceptions import HTTPException

@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "index"

    @app.route("/after_this_request")
    def after_this_request_route():
        @after_this_request
        def add_header(response):
            response.headers['X-Foo'] = 'Bar'
            return response
        return "after_this_request"

    @app.route("/copy_context")
    def copy_context_route():
        @copy_current_request_context
        def do_some_work():
            assert has_request_context()
            assert has_app_context()
        do_some_work()
        return "copy_context"

    return app

def test_app_ctx_globals() -> None:
    g = _AppCtxGlobals()
    g.test = "value"
    assert g.test == "value"
    assert g.get("test") == "value"
    assert g.get("missing", "default") == "default"
    g.pop("test")
    with pytest.raises(AttributeError):
        g.test

def test_app_context(app: Flask) -> None:
    with app.app_context():
        assert has_app_context()
        assert not has_request_context()

def test_request_context(app: Flask) -> None:
    with app.test_request_context('/'):
        assert has_request_context()
        assert has_app_context()

def test_after_this_request(app: Flask) -> None:
    test_client = app.test_client()
    response = test_client.get("/after_this_request")
    assert response.status_code == 200
    assert response.headers['X-Foo'] == 'Bar'

def test_copy_current_request_context(app: Flask) -> None:
    test_client = app.test_client()
    response = test_client.get("/copy_context")
    assert response.status_code == 200

def test_has_request_context(app: Flask) -> None:
    with app.test_request_context('/'):
        assert has_request_context()

def test_has_app_context(app: Flask) -> None:
    with app.app_context():
        assert has_app_context()

def test_app_ctx_globals_repr(app: Flask) -> None:
    with app.app_context():
        assert repr(g) == f"<flask.g of '{app.name}'>"

def test_request_context_repr(app: Flask) -> None:
    with app.test_request_context('/'):
        ctx = _cv_request.get()
        assert repr(ctx) == f"<RequestContext '/' [GET] of {app.name}>"

def test_app_context_push_pop(app: Flask) -> None:
    ctx = AppContext(app)
    ctx.push()
    assert has_app_context()
    ctx.pop()
    assert not has_app_context()

def test_request_context_push_pop(app: Flask) -> None:
    ctx = RequestContext(app, app.test_request_context('/').request)
    ctx.push()
    assert has_request_context()
    ctx.pop()
    assert not has_request_context()

def test_after_this_request_no_context(app: Flask) -> None:
    with pytest.raises(RuntimeError):
        after_this_request(lambda response: response)

def test_copy_current_request_context_no_context(app: Flask) -> None:
    with pytest.raises(RuntimeError):
        copy_current_request_context(lambda: None)

def test_app_context_pop_exception(app: Flask) -> None:
    ctx = AppContext(app)
    ctx.push()
    with pytest.raises(AssertionError):
        ctx.pop()
        ctx.pop()

def test_request_context_pop_exception(app: Flask) -> None:
    ctx = RequestContext(app, app.test_request_context('/').request)
    ctx.push()
    with pytest.raises(AssertionError):
        ctx.pop()
        ctx.pop()