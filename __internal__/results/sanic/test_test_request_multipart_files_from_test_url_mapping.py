import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('payload,filename', [
    ('------sanic\r\nContent-Disposition: form-data; filename="filename"; name="test"\r\n\r\nOK\r\n------sanic--\r\n', 'filename'),
    ('------sanic\r\nContent-Disposition: form-data; filename=""; name="test"\r\n\r\nOK\r\n------sanic--\r\n', ''),
    ('------sanic\r\nContent-Disposition: form-data; filename*="utf-8\'\'filename_%C2%A0_test"; name="test"\r\n\r\nOK\r\n------sanic--\r\n', 'filename_ _test'),
])
def test_post_method_with_multipart_files(app, payload, filename):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text('I am post method')

    headers = {"content-type": "multipart/form-data; boundary=----sanic"}

    request, response = app.test_client.post(data=payload, headers=headers)
    assert response.status == 200
    assert request.files.get("test").name == filename

def test_post_method_empty_file(app):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text('I am post method')

    payload = '------sanic\r\nContent-Disposition: form-data; filename=""; name="test"\r\n\r\n\r\n------sanic--\r\n'
    headers = {"content-type": "multipart/form-data; boundary=----sanic"}

    request, response = app.test_client.post(data=payload, headers=headers)
    assert response.status == 200
    assert request.files.get("test").name == ''

def test_post_method_invalid_content_type(app):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text('I am post method')

    payload = 'Invalid payload'
    headers = {"content-type": "text/plain"}

    request, response = app.test_client.post(data=payload, headers=headers)
    assert response.status == 200
    assert request.files.get("test") is None

def test_post_method_no_file(app):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text('I am post method')

    payload = '------sanic\r\nContent-Disposition: form-data; name="test"\r\n\r\nNo file\r\n------sanic--\r\n'
    headers = {"content-type": "multipart/form-data; boundary=----sanic"}

    request, response = app.test_client.post(data=payload, headers=headers)
    assert response.status == 200
    assert request.files.get("test") is None