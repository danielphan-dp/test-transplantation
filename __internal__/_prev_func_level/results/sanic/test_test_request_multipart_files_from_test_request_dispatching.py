import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('payload,filename', [
    ('------sanic\r\nContent-Disposition: form-data; filename="testfile"; name="test"\r\n\r\nContent\r\n------sanic--\r\n', 'testfile'),
    ('------sanic\r\nContent-Disposition: form-data; filename=""; name="test"\r\n\r\nContent\r\n------sanic--\r\n', ''),
    ('------sanic\r\nContent-Disposition: form-data; filename="file_with_special_chars_ä_test"; name="test"\r\n\r\nContent\r\n------sanic--\r\n', 'file_with_special_chars_ä_test'),
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

def test_post_method_no_file(app):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text('I am post method')

    payload = '------sanic\r\nContent-Disposition: form-data; name="test"\r\n\r\nContent\r\n------sanic--\r\n'
    headers = {"content-type": "multipart/form-data; boundary=----sanic"}

    request, response = app.test_client.post(data=payload, headers=headers)
    assert response.status == 200
    assert request.files.get("test") is None

def test_post_method_invalid_boundary(app):
    @app.route("/", methods=["POST"])
    async def post(request):
        return text('I am post method')

    payload = '------invalid_boundary\r\nContent-Disposition: form-data; filename="testfile"; name="test"\r\n\r\nContent\r\n------invalid_boundary--\r\n'
    headers = {"content-type": "multipart/form-data; boundary=----invalid_boundary"}

    request, response = app.test_client.post(data=payload, headers=headers)
    assert response.status == 400  # Expecting a bad request due to invalid boundary