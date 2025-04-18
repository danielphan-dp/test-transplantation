# Transplanted from tests/test_basic.py in Quart to test Flask functionality in src/flask/app.py

from __future__ import annotations

import pytest
from flask import Flask, jsonify, request, url_for, abort, Response
from werkzeug.wrappers import Response as WerkzeugResponse

@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index() -> str:
        return "index"

    @app.route("/❤️")
    def iri() -> str:
        return "💔"

    @app.route("/sync/")
    def sync() -> str:
        return "index"

    @app.route("/json/", methods=["POST"])
    def json() -> Response:
        data = request.get_json()
        return jsonify(data)

    @app.route("/implicit_json/", methods=["POST"])
    def implicit_json() -> Response:
        data = request.get_json()
        return jsonify(data)

    @app.route("/werkzeug/")
    def werkzeug() -> WerkzeugResponse:
        return WerkzeugResponse(b"Hello")

    @app.route("/error/")
    def error() -> str:
        abort(409)
        return "OK"

    @app.route("/param/<value>")
    def param(value: str) -> str:
        return value

    @app.route("/stream")
    def stream() -> Response:
        def _gen():
            yield "Hello "
            yield "World"
        return Response(_gen(), mimetype='text/plain')

    @app.errorhandler(409)
    def generic_http_handler(_: Exception) -> tuple[str, int]:
        return "Something Unique", 409

    @app.errorhandler(404)
    def not_found_handler(_: Exception) -> tuple[str, int]:
        return "Not Found", 404

    return app


@pytest.mark.parametrize("path", ["/", "/sync/"])
def test_index(path: str, app: Flask) -> None:
    test_client = app.test_client()
    response = test_client.get(path)
    assert response.status_code == 200
    assert b"index" in response.data


def test_iri(app: Flask) -> None:
    test_client = app.test_client()
    response = test_client.get("/❤️")
    assert "💔".encode() in response.data


def test_options(app: Flask) -> None:
    test_client = app.test_client()
    response = test_client.options("/")
    assert response.status_code == 200
    assert {method.strip() for method in response.headers["Allow"].split(",")} == {
        "HEAD",
        "OPTIONS",
        "GET",
    }


def test_json(app: Flask) -> None:
    test_client = app.test_client()
    response = test_client.post("/json/", json={"value": "json"})
    assert response.status_code == 200
    assert b'{"value":"json"}\n' == response.data


def test_implicit_json(app: Flask) -> None:
    test_client = app.test_client()
    response = test_client.post("/implicit_json/", json={"value": "json"})
    assert response.status_code == 200
    assert b'{"value":"json"}\n' == response.data


def test_werkzeug(app: Flask) -> None:
    test_client = app.test_client()
    response = test_client.get("/werkzeug/")
    assert response.status_code == 200
    assert b"Hello" == response.data


def test_generic_error(app: Flask) -> None:
    test_client = app.test_client()
    response = test_client.get("/error/")
    assert response.status_code == 409
    assert b"Something Unique" in response.data


def test_url_defaults(app: Flask) -> None:
    @app.url_defaults
    def defaults(_: str, values: dict) -> None:
        values["value"] = "hello"

    with app.test_request_context("/"):
        assert url_for("param") == "/param/hello"


def test_not_found_error(app: Flask) -> None:
    test_client = app.test_client()
    response = test_client.get("/not_found/")
    assert response.status_code == 404
    assert b"Not Found" in response.data


def test_make_response_str(app: Flask) -> None:
    response = app.make_response("Result")
    assert response.status_code == 200
    assert response.data == b"Result"

    response = app.make_response(("Result", 200))
    response = app.make_response(("Result", {"name": "value"}))
    assert response.status_code == 200
    assert response.data == b"Result"
    assert response.headers["name"] == "value"

    response = app.make_response(("Result", 404, {"name": "value"}))
    assert response.status_code == 404
    assert response.data == b"Result"
    assert response.headers["name"] == "value"


def test_make_response_response(app: Flask) -> None:
    response = app.make_response(Response("Result"))
    assert response.status_code == 200
    assert response.data == b"Result"

    response = app.make_response((Response("Result"), {"name": "value"}))
    assert response.status_code == 200
    assert response.data == b"Result"
    assert response.headers["name"] == "value"

    response = app.make_response((Response("Result"), 404, {"name": "value"}))
    assert response.status_code == 404
    assert response.data == b"Result"
    assert response.headers["name"] == "value"


def test_make_response_errors(app: Flask) -> None:
    with pytest.raises(TypeError):
        app.make_response(("Result", {"name": "value"}, 200))  # type: ignore
    with pytest.raises(TypeError):
        app.make_response(("Result", {"name": "value"}, 200, "a"))  # type: ignore
    with pytest.raises(TypeError):
        app.make_response(("Result",))  # type: ignore


def test_root_path(app: Flask) -> None:
    test_client = app.test_client()
    response = test_client.get("/", root_path="/bob")
    assert response.status_code == 404
    response = test_client.get("/bob/", root_path="/bob")
    assert response.status_code == 200


def test_stream(app: Flask) -> None:
    test_client = app.test_client()
    response = test_client.get("/stream")
    assert response.data == b"Hello World"