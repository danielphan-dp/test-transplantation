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

def test_request_multipart_file_empty(app):
    payload = (
        "--e73ffaa8b1b2472b8ec848de833cb05b\r\n"
        'Content-Disposition: form-data; name="file"\r\n'
        "\r\n"
        "--e73ffaa8b1b2472b8ec848de833cb05b--\r\n"
    )
    headers = {
        "Content-Type": "multipart/form-data;"
        " boundary=e73ffaa8b1b2472b8ec848de833cb05b"
    }
    request, _ = app.test_client.post(data=payload, headers=headers)
    assert request.form.getlist("file") == []

def test_request_multipart_file_single_file(app):
    payload = (
        "--e73ffaa8b1b2472b8ec848de833cb05b\r\n"
        'Content-Disposition: form-data; name="file"\r\n'
        "Content-Type: application/octet-stream\r\n"
        "Content-Length: 15\r\n"
        "\r\n"
        '{"test":"json"}\r\n'
        "--e73ffaa8b1b2472b8ec848de833cb05b--\r\n"
    )
    headers = {
        "Content-Type": "multipart/form-data;"
        " boundary=e73ffaa8b1b2472b8ec848de833cb05b"
    }
    request, _ = app.test_client.post(data=payload, headers=headers)
    assert request.form.getlist("file") == ['{"test":"json"}']

def test_request_multipart_file_invalid_format(app):
    payload = "invalid_format_data"
    headers = {
        "Content-Type": "application/octet-stream"
    }
    request, _ = app.test_client.post(data=payload, headers=headers)
    assert request.status == 400

def test_request_multipart_file_large_file(app):
    large_payload = (
        "--e73ffaa8b1b2472b8ec848de833cb05b\r\n"
        'Content-Disposition: form-data; name="file"\r\n'
        "Content-Type: application/octet-stream\r\n"
        "Content-Length: 1000000\r\n"
        "\r\n"
        'A' * 1000000 + "\r\n"
        "--e73ffaa8b1b2472b8ec848de833cb05b--\r\n"
    )
    headers = {
        "Content-Type": "multipart/form-data;"
        " boundary=e73ffaa8b1b2472b8ec848de833cb05b"
    }
    request, _ = app.test_client.post(data=large_payload, headers=headers)
    assert request.status == 200

def test_request_multipart_file_duplicate_field_name(app):
    payload = (
        "--e73ffaa8b1b2472b8ec848de833cb05b\r\n"
        'Content-Disposition: form-data; name="file"\r\n'
        "Content-Type: application/octet-stream\r\n"
        "Content-Length: 15\r\n"
        "\r\n"
        '{"test":"json"}\r\n'
        "--e73ffaa8b1b2472b8ec848de833cb05b\r\n"
        'Content-Disposition: form-data; name="file"\r\n'
        "Content-Type: application/octet-stream\r\n"
        "Content-Length: 15\r\n"
        "\r\n"
        '{"test":"json2"}\r\n'
        "--e73ffaa8b1b2472b8ec848de833cb05b--\r\n"
    )
    headers = {
        "Content-Type": "multipart/form-data;"
        " boundary=e73ffaa8b1b2472b8ec848de833cb05b"
    }
    request, _ = app.test_client.post(data=payload, headers=headers)
    assert request.form.getlist("file") == [
        '{"test":"json"}',
        '{"test":"json2"}',
    ]