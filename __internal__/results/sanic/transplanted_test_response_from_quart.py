# Transplanted from tests/wrappers/test_response.py to sanic/response/__init__.py

import pytest
from sanic.response import (
    BaseHTTPResponse,
    HTTPResponse,
    JSONResponse,
    ResponseStream,
    empty,
    file,
    file_stream,
    html,
    json,
    raw,
    redirect,
    text,
    validate_file,
    json_dumps,
)
from io import BytesIO
from pathlib import Path

# Test the empty response function
def test_empty_response():
    response = empty()
    assert response.status == 204
    assert response.body == b""

# Test the text response function
def test_text_response():
    response = text("Hello, world!")
    assert response.status == 200
    assert response.body == b"Hello, world!"
    assert response.content_type == "text/plain; charset=utf-8"

# Test the json response function
def test_json_response():
    response = json({"message": "Hello, world!"})
    assert response.status == 200
    assert response.body == b'{"message":"Hello, world!"}'
    assert response.content_type == "application/json"

# Test the html response function
def test_html_response():
    response = html("<p>Hello, world!</p>")
    assert response.status == 200
    assert response.body == b"<p>Hello, world!</p>"
    assert response.content_type == "text/html; charset=utf-8"

# Test the raw response function
def test_raw_response():
    response = raw(b"raw data")
    assert response.status == 200
    assert response.body == b"raw data"
    assert response.content_type == "application/octet-stream"

# Test the redirect response function
def test_redirect_response():
    response = redirect("/new-location")
    assert response.status == 302
    assert response.headers["Location"] == "/new-location"

# Test the file response function
def test_file_response(tmp_path: Path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("file content")
    response = file(file_path)
    assert response.status == 200
    assert response.body == b"file content"
    assert response.content_type == "text/plain; charset=utf-8"

# Test the file_stream response function
async def test_file_stream_response(tmp_path: Path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("file content")
    response = await file_stream(file_path)
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    body = b"".join([chunk async for chunk in response.stream()])
    assert body == b"file content"

# Test the validate_file function
def test_validate_file(tmp_path: Path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("file content")
    assert validate_file(file_path) is True

# Test the json_dumps function
def test_json_dumps():
    data = {"key": "value"}
    result = json_dumps(data)
    assert result == '{"key":"value"}'