# This test file was generated from tests/test_ctx.py to test the functionality in src/flask/ctx.py through test transplantation.

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
from flask.testing import make_test_headers_path_and_query_string
from flask.wrappers import Request


@pytest.fixture
def app():
    app = Flask(__name__)
    return app


@pytest.fixture
def http_scope():
    return {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "server": ("127.0.0.1", 5000),
        "client": ("127.0.0.1", 12345),
        "scheme": "http",
        "method": "GET",
        "root_path": "",
        "path": "/",
        "raw_path": b"/",
        "query_string": b"",
        "headers": [],
    }


async def test_request_context_match(app, http_scope) -> None:
    url_adapter = Mock()
    rule = Mock()
    rule.endpoint = "index"
    url_adapter.match.return_value = (rule, {"arg": "value"})
    app.create_url_adapter = lambda *_: url_adapter  # type: ignore
    request = Request(
        http_scope,
        b"",
        Headers([("host", "flask.com")]),
    )
    with RequestContext(app, request):
        assert request.url_rule == rule
        assert request.view_args == {"arg": "value"}


async def test_bad_request_if_websocket_route(app, http_scope) -> None:
    url_adapter = Mock()
    url_adapter.match.side_effect = BadRequest()
    app.create_url_adapter = lambda *_: url_adapter  # type: ignore
    request = Request(
        http_scope,
        b"",
        Headers([("host", "flask.com")]),
    )
    with RequestContext(app, request):
        assert isinstance(request.routing_exception, BadRequest)


async def test_after_this_request(app, http_scope) -> None:
    headers, path, query_string = make_test_headers_path_and_query_string(app, "/")
    with RequestContext(
        app,
        Request(
            http_scope,
            query_string,
            headers,
        ),
    ) as context:
        after_this_request(lambda response: "hello")  # type: ignore
        assert context._after_request_functions[0](None) == "hello"  # type: ignore


async def test_has_request_context(app, http_scope) -> None:
    headers, path, query_string = make_test_headers_path_and_query_string(app, "/")
    request = Request(
        http_scope,
        query_string,
        headers,
    )
    with RequestContext(app, request):
        assert has_request_context() is True
        assert has_app_context() is True
    assert has_request_context() is False
    assert has_app_context() is False


async def test_has_app_context(app) -> None:
    with AppContext(app):
        assert has_app_context() is True
    assert has_app_context() is False


async def test_copy_current_app_context(app) -> None:
    @app.route("/")
    def index() -> str:
        g.foo = "bar"

        @copy_current_app_context
        async def within_context() -> None:
            assert g.foo == "bar"

        await asyncio.ensure_future(within_context())
        return ""

    test_client = app.test_client()
    response = await test_client.get("/")
    assert response.status_code == 200


def test_copy_current_app_context_error() -> None:
    with pytest.raises(RuntimeError):
        copy_current_app_context(lambda: None)()


async def test_copy_current_request_context(app) -> None:
    @app.route("/")
    def index() -> str:
        @copy_current_request_context
        async def within_context() -> None:
            assert request.path == "/"

        await asyncio.ensure_future(within_context())
        return ""

    test_client = app.test_client()
    response = await test_client.get("/")
    assert response.status_code == 200


def test_copy_current_request_context_error() -> None:
    with pytest.raises(RuntimeError):
        copy_current_request_context(lambda: None)()