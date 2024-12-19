import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('payload,filename', [
    ('------sanic\r\nContent-Disposition: form-data; filename="valid_file.txt"; name="test"\r\n\r\nContent of the file\r\n------sanic--\r\n', 'valid_file.txt'),
    ('------sanic\r\nContent-Disposition: form-data; filename=""; name="test"\r\n\r\n\r\n------sanic--\r\n', ''),
    ('------sanic\r\nContent-Disposition: form-data; filename="invalid_file.txt"; name="test"\r\n\r\n\r\n------sanic--\r\n', 'invalid_file.txt'),
    ('------sanic\r\nContent-Disposition: form-data; filename="filename_with_special_chars_ä_test"; name="test"\r\n\r\nContent with special chars\r\n------sanic--\r\n', 'filename_with_special_chars_ä_test'),
])
def test_post_method_with_multipart_files(app, payload, filename):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text("I am post method")

    headers = {"content-type": "multipart/form-data; boundary=----sanic"}

    request, _ = app.test_client.post(data=payload, headers=headers)
    assert request.files.get("test").name == filename

def test_post_method_empty_file(app):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text("I am post method")

    payload = '------sanic\r\nContent-Disposition: form-data; filename=""; name="test"\r\n\r\n\r\n------sanic--\r\n'
    headers = {"content-type": "multipart/form-data; boundary=----sanic"}

    request, _ = app.test_client.post(data=payload, headers=headers)
    assert request.files.get("test").name == ''

def test_post_method_no_file(app):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text("I am post method")

    payload = '------sanic\r\nContent-Disposition: form-data; name="test"\r\n\r\nNo file here\r\n------sanic--\r\n'
    headers = {"content-type": "multipart/form-data; boundary=----sanic"}

    request, _ = app.test_client.post(data=payload, headers=headers)
    assert request.files.get("test") is None

def test_post_method_with_large_file(app):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text("I am post method")

    large_content = 'A' * 10**6  # 1 MB of data
    payload = f'------sanic\r\nContent-Disposition: form-data; filename="large_file.txt"; name="test"\r\n\r\n{large_content}\r\n------sanic--\r\n'
    headers = {"content-type": "multipart/form-data; boundary=----sanic"}

    request, _ = app.test_client.post(data=payload, headers=headers)
    assert request.files.get("test").name == 'large_file.txt'