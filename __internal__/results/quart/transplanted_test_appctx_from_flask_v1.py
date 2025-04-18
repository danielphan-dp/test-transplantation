# Transplanted from tests/test_appctx.py to test src/quart/ctx.py

import pytest
from quart import Quart, url_for, g
from quart.ctx import AppContext, RequestContext, has_app_context, has_request_context

@pytest.fixture
def app():
    app = Quart(__name__)
    app.config["SERVER_NAME"] = "localhost"
    app.config["PREFERRED_URL_SCHEME"] = "https"

    @app.route("/")
    async def index():
        return "Hello, World!"

    return app

def test_basic_url_generation(app):
    """Test URL generation within an app context."""
    with app.app_context():
        rv = url_for("index")
        assert rv == "https://localhost/"

def test_url_generation_requires_server_name(app):
    """Test URL generation raises error without SERVER_NAME."""
    app.config.pop("SERVER_NAME", None)
    with app.app_context():
        with pytest.raises(RuntimeError):
            url_for("index")

def test_url_generation_without_context_fails():
    """Test URL generation fails without an app context."""
    with pytest.raises(RuntimeError):
        url_for("index")

def test_request_context_means_app_context(app):
    """Test that a request context implies an app context."""
    with app.test_request_context():
        assert has_app_context()
    assert not has_app_context()

def test_app_context_provides_current_app(app):
    """Test that the app context provides the current app."""
    with app.app_context():
        assert has_app_context()
    assert not has_app_context()

def test_app_tearing_down(app):
    """Test app context teardown."""
    cleanup_stuff = []

    @app.teardown_appcontext
    async def cleanup(exception):
        cleanup_stuff.append(exception)

    with app.app_context():
        pass

    assert cleanup_stuff == [None]

def test_app_tearing_down_with_previous_exception(app):
    """Test app context teardown with a previous exception."""
    cleanup_stuff = []

    @app.teardown_appcontext
    async def cleanup(exception):
        cleanup_stuff.append(exception)

    try:
        raise Exception("dummy")
    except Exception:
        pass

    with app.app_context():
        pass

    assert cleanup_stuff == [None]

def test_app_tearing_down_with_handled_exception_by_except_block(app):
    """Test app context teardown with handled exception."""
    cleanup_stuff = []

    @app.teardown_appcontext
    async def cleanup(exception):
        cleanup_stuff.append(exception)

    with app.app_context():
        try:
            raise Exception("dummy")
        except Exception:
            pass

    assert cleanup_stuff == [None]

def test_app_tearing_down_with_unhandled_exception(app):
    """Test app context teardown with unhandled exception."""
    cleanup_stuff = []

    @app.teardown_appcontext
    async def cleanup(exception):
        cleanup_stuff.append(exception)

    @app.route("/error")
    async def error():
        raise ValueError("dummy")

    with pytest.raises(ValueError, match="dummy"):
        with app.test_client() as client:
            client.get("/error")

    assert len(cleanup_stuff) == 1
    assert isinstance(cleanup_stuff[0], ValueError)
    assert str(cleanup_stuff[0]) == "dummy"

def test_app_ctx_globals_methods(app):
    """Test methods on the app context globals."""
    with app.app_context():
        # get
        assert g.get("foo") is None
        assert g.get("foo", "bar") == "bar"
        # __contains__
        assert "foo" not in g
        g.foo = "bar"
        assert "foo" in g
        # setdefault
        g.setdefault("bar", "the cake is a lie")
        g.setdefault("bar", "hello world")
        assert g.bar == "the cake is a lie"
        # pop
        assert g.pop("bar") == "the cake is a lie"
        with pytest.raises(KeyError):
            g.pop("bar")
        assert g.pop("bar", "more cake") == "more cake"
        # __iter__
        assert list(g) == ["foo"]
        # __repr__
        assert repr(g) == "<quart.g of 'quart_test'>"

def test_custom_app_ctx_globals_class(app):
    """Test using a custom app context globals class."""
    class CustomAppGlobals:
        def __init__(self):
            self.spam = "eggs"

    app.app_ctx_globals_class = CustomAppGlobals
    with app.app_context():
        assert g.spam == "eggs"

def test_context_refcounts(app):
    """Test reference counting for contexts."""
    called = []

    @app.teardown_request
    async def teardown_req(error=None):
        called.append("request")

    @app.teardown_appcontext
    async def teardown_app(error=None):
        called.append("app")

    @app.route("/")
    async def index():
        with app.app_context():
            with app.test_request_context():
                pass
        return ""

    with app.test_client() as client:
        res = client.get("/")
        assert res.status_code == 200
        assert res.data == b""
        assert called == ["request", "app"]

def test_clean_pop(app):
    """Test clean pop of app context."""
    called = []

    @app.teardown_request
    async def teardown_req(error=None):
        raise ZeroDivisionError

    @app.teardown_appcontext
    async def teardown_app(error=None):
        called.append("TEARDOWN")

    with app.app_context():
        called.append(app.name)

    assert called == ["quart_test", "TEARDOWN"]
    assert not has_app_context()