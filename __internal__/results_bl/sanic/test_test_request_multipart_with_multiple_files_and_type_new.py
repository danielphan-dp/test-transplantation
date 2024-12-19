import base64
import logging
import json
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/", methods=["POST"])
    async def post(request):
        return text("I am post method")
    return app

def test_request_multipart_with_no_files(app):
    payload = '------sanic\r\nContent-Disposition: form-data; name="file";\r\n\r\n------sanic--'
    headers = {"content-type": "multipart/form-data; boundary=------sanic"}

    request, _ = app.test_client.post(data=payload, headers=headers)
    assert len(request.files.getlist("file")) == 0

def test_request_multipart_with_single_file(app):
    payload = (
        '------sanic\r\nContent-Disposition: form-data; name="file";'
        ' filename="test.json"\r\nContent-Type: application/json\r\n\r\n{"key": "value"}\r\n'
        '------sanic--'
    )
    headers = {"content-type": "multipart/form-data; boundary=------sanic"}

    request, _ = app.test_client.post(data=payload, headers=headers)
    assert len(request.files.getlist("file")) == 1
    assert request.files.getlist("file")[0].type == "application/json"

def test_request_multipart_with_invalid_file_type(app):
    payload = (
        '------sanic\r\nContent-Disposition: form-data; name="file";'
        ' filename="test.txt"\r\nContent-Type: text/plain\r\n\r\nSample text content\r\n'
        '------sanic--'
    )
    headers = {"content-type": "multipart/form-data; boundary=------sanic"}

    request, _ = app.test_client.post(data=payload, headers=headers)
    assert len(request.files.getlist("file")) == 1
    assert request.files.getlist("file")[0].type == "text/plain"

def test_request_multipart_with_large_file(app):
    large_content = 'A' * (10**6)  # 1 MB of data
    payload = (
        '------sanic\r\nContent-Disposition: form-data; name="file";'
        ' filename="large_file.bin"\r\nContent-Type: application/octet-stream\r\n\r\n'
        f'{large_content}\r\n------sanic--'
    )
    headers = {"content-type": "multipart/form-data; boundary=------sanic"}

    request, _ = app.test_client.post(data=payload, headers=headers)
    assert len(request.files.getlist("file")) == 1
    assert request.files.getlist("file")[0].type == "application/octet-stream"