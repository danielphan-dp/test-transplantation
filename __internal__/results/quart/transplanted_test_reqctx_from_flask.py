# Transplanted from tests/test_reqctx.py to test src/quart/ctx.py

import pytest
from quart import Quart, request, has_request_context, has_app_context
from quart.ctx import RequestContext, AppContext
from quart.sessions import SecureCookieSessionInterface, SessionInterface
from quart.globals import _cv_request, _cv_app

# Test to ensure that the request context is properly torn down
def test_teardown_on_pop():
    app = Quart(__name__)
    buffer = []

    @app.teardown_request
    async def end_of_request(exception):
        buffer.append(exception)

    ctx = app.test_request_context()
    ctx.push()
    assert buffer == []
    ctx.pop()
    assert buffer == [None]

# Test to ensure that the request context is properly torn down with a previous exception
def test_teardown_with_previous_exception():
    app = Quart(__name__)
    buffer = []

    @app.teardown_request
    async def end_of_request(exception):
        buffer.append(exception)

    try:
        raise Exception("dummy")
    except Exception:
        pass

    with app.test_request_context():
        assert buffer == []
    assert buffer == [None]

# Test to ensure that the request context is properly torn down with a handled exception
def test_teardown_with_handled_exception():
    app = Quart(__name__)
    buffer = []

    @app.teardown_request
    async def end_of_request(exception):
        buffer.append(exception)

    with app.test_request_context():
        assert buffer == []
        try:
            raise Exception("dummy")
        except Exception:
            pass
    assert buffer == [None]

# Test to ensure that the request context is properly bound
def test_context_binding():
    app = Quart(__name__)

    @app.route("/")
    async def index():
        return f"Hello {request.args['name']}!"

    @app.route("/meh")
    async def meh():
        return request.url

    with app.test_request_context("/?name=World"):
        assert index() == "Hello World!"
    with app.test_request_context("/meh"):
        assert meh() == "http://localhost/meh"
    assert not request

# Test to ensure that the request context is properly tested
def test_context_test():
    app = Quart(__name__)
    assert not request
    assert not has_request_context()
    ctx = app.test_request_context()
    ctx.push()
    try:
        assert request
        assert has_request_context()
    finally:
        ctx.pop()

# Test to ensure that the request context is manually bound
def test_manual_context_binding():
    app = Quart(__name__)

    @app.route("/")
    async def index():
        return f"Hello {request.args['name']}!"

    ctx = app.test_request_context("/?name=World")
    ctx.push()
    assert index() == "Hello World!"
    ctx.pop()
    with pytest.raises(RuntimeError):
        index()

# Test to ensure that the session error pops the context
def test_session_error_pops_context():
    class SessionError(Exception):
        pass

    class FailingSessionInterface(SessionInterface):
        async def open_session(self, app, request):
            raise SessionError()

    class CustomQuart(Quart):
        session_interface = FailingSessionInterface()

    app = CustomQuart(__name__)

    @app.route("/")
    async def index():
        # shouldn't get here
        AssertionError()

    response = app.test_client().get("/")
    assert response.status_code == 500
    assert not request
    assert not has_app_context()

# Test to ensure that the session dynamic cookie name works
def test_session_dynamic_cookie_name():
    class PathAwareSessionInterface(SecureCookieSessionInterface):
        def get_cookie_name(self, app):
            if request.url.endswith("dynamic_cookie"):
                return "dynamic_cookie_name"
            else:
                return super().get_cookie_name(app)

    class CustomQuart(Quart):
        session_interface = PathAwareSessionInterface()

    app = CustomQuart(__name__)
    app.secret_key = "secret_key"

    @app.route("/set", methods=["POST"])
    async def set():
        request.session["value"] = request.form["value"]
        return "value set"

    @app.route("/get")
    async def get():
        v = request.session.get("value", "None")
        return v

    @app.route("/set_dynamic_cookie", methods=["POST"])
    async def set_dynamic_cookie():
        request.session["value"] = request.form["value"]
        return "value set"

    @app.route("/get_dynamic_cookie")
    async def get_dynamic_cookie():
        v = request.session.get("value", "None")
        return v

    test_client = app.test_client()

    # first set the cookie in both /set urls but each with a different value
    assert test_client.post("/set", data={"value": "42"}).data == b"value set"
    assert (
        test_client.post("/set_dynamic_cookie", data={"value": "616"}).data
        == b"value set"
    )

    # now check that the relevant values come back - meaning that different
    # cookies are being used for the urls that end with "dynamic cookie"
    assert test_client.get("/get").data == b"42"
    assert test_client.get("/get_dynamic_cookie").data == b"616"