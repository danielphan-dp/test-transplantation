# This test file was generated from tests/test_ctx.py in the donor project to test src/flask/ctx.py in the host project through test transplantation.

from __future__ import annotations

import asyncio
from unittest.mock import Mock

import pytest
from werkzeug.datastructures import Headers
from werkzeug.exceptions import BadRequest

from flask import Flask, g, request
from flask.ctx import (
    after_this_request,
    AppContext,
    copy_current_app_context,
    copy_current_request_context,
    has_app_context,
    has_request_context,
    RequestContext,
)
from flask.globals import _cv_request
from flask.sessions import SessionMixin
from flask.signals import appcontext_pushed, appcontext_popped
from flask.typing import WSGIEnvironment
from flask.wrappers import Request


# Mocking a WSGI environment for testing
def make_test_environ() -> WSGIEnvironment:
    return {
        "REQUEST_METHOD": "GET",
        "PATH_INFO": "/",
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "5000",
        "wsgi.url_scheme": "http",
    }


async def test_request_context_match() -> None:
    app = Flask(__name__)
    url_adapter = Mock()
    rule = Mock()
    rule.endpoint = "index"
    url_adapter.match.return_value = (rule, {"arg": "value"})
    app.create_url_adapter = lambda *_: url_adapter  # type: ignore
    environ = make_test_environ()
    request = Request(environ)
    with RequestContext(app, environ, request):
        assert request.url_rule == rule
        assert request.view_args == {"arg": "value"}


async def test_bad_request_if_websocket_route() -> None:
    app = Flask(__name__)
    url_adapter = Mock()
    url_adapter.match.side_effect = BadRequest()
    app.create_url_adapter = lambda *_: url_adapter  # type: ignore
    environ = make_test_environ()
    request = Request(environ)
    with RequestContext(app, environ, request):
        assert isinstance(request.routing_exception, BadRequest)


async def test_after_this_request() -> None:
    app = Flask(__name__)
    environ = make_test_environ()
    with RequestContext(app, environ, Request(environ)) as context:
        after_this_request(lambda response: "hello")  # type: ignore
        assert context._after_request_functions[0](None) == "hello"  # type: ignore


async def test_has_request_context() -> None:
    app = Flask(__name__)
    environ = make_test_environ()
    with RequestContext(app, environ, Request(environ)):
        assert has_request_context() is True
        assert has_app_context() is True
    assert has_request_context() is False
    assert has_app_context() is False


async def test_has_app_context() -> None:
    app = Flask(__name__)
    with AppContext(app):
        assert has_app_context() is True
    assert has_app_context() is False


async def test_copy_current_app_context() -> None:
    app = Flask(__name__)

    @app.route("/")
    def index() -> str:
        g.foo = "bar"

        @copy_current_app_context
        def within_context() -> None:
            assert g.foo == "bar"

        asyncio.ensure_future(within_context())
        return ""

    test_client = app.test_client()
    response = test_client.get("/")
    assert response.status_code == 200


def test_copy_current_app_context_error() -> None:
    with pytest.raises(RuntimeError):
        copy_current_app_context(lambda: None)()


async def test_copy_current_request_context() -> None:
    app = Flask(__name__)

    @app.route("/")
    def index() -> str:
        @copy_current_request_context
        def within_context() -> None:
            assert request.path == "/"

        asyncio.ensure_future(within_context())
        return ""

    test_client = app.test_client()
    response = test_client.get("/")
    assert response.status_code == 200


def test_copy_current_request_context_error() -> None:
    with pytest.raises(RuntimeError):
        copy_current_request_context(lambda: None)()


async def test_works_without_copy_current_request_context() -> None:
    app = Flask(__name__)

    @app.route("/")
    def index() -> str:
        def within_context() -> None:
            assert request.path == "/"

        asyncio.ensure_future(within_context())
        return ""

    test_client = app.test_client()
    response = test_client.get("/")
    assert response.status_code == 200