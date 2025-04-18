# This test file was generated from tests/wrappers/test_response.py to test sanic/response/convenience.py through test transplantation.

import pytest
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from sanic.response.convenience import (
    empty,
    json,
    text,
    raw,
    html,
    validate_file,
    file,
    redirect,
    file_stream,
)
from sanic.models.protocol_types import Range
from sanic.compat import Header
from sanic.helpers import Default

# Test the empty response function
def test_empty_response():
    response = empty()
    assert response.status == 204
    assert response.body == b""

# Test the JSON response function
def test_json_response():
    response = json({"key": "value"})
    assert response.status == 200
    assert response.content_type == "application/json"
    assert response.body == b'{"key": "value"}'

# Test the text response function
def test_text_response():
    response = text("Hello, World!")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.body == "Hello, World!"

# Test the raw response function
def test_raw_response():
    response = raw(b"raw data")
    assert response.status == 200
    assert response.content_type == "application/octet-stream"
    assert response.body == b"raw data"

# Test the HTML response function
def test_html_response():
    response = html("<h1>Hello</h1>")
    assert response.status == 200
    assert response.content_type == "text/html; charset=utf-8"
    assert response.body == "<h1>Hello</h1>"

# Test the redirect function
def test_redirect():
    response = redirect("/new-location")
    assert response.status == 302
    assert response.headers["Location"] == "/new-location"

# Test the validate_file function
@pytest.mark.asyncio
async def test_validate_file():
    headers = Header({"If-Modified-Since": "Wed, 21 Oct 2015 07:28:00 GMT"})
    last_modified = datetime(2015, 10, 21, 7, 28, tzinfo=timezone.utc)
    response = await validate_file(headers, last_modified)
    assert response.status == 304

# Test the file response function
@pytest.mark.asyncio
async def test_file_response(tmp_path: Path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("file content")
    response = await file(file_path)
    assert response.status == 200
    assert response.body == b"file content"

# Test the file_stream response function
@pytest.mark.asyncio
async def test_file_stream_response(tmp_path: Path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("stream content")
    response = await file_stream(file_path)
    chunks = []
    async for chunk in response.streaming_fn(response):
        chunks.append(chunk)
    assert b"".join(chunks) == b"stream content"