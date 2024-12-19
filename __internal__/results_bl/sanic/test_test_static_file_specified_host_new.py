import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png', '', 'nonexistent.file'])
def test_get_file_path(app, static_file_directory, file_name):
    if file_name == '':
        expected_path = os.path.join(static_file_directory, '')
    else:
        expected_path = os.path.join(static_file_directory, file_name)

    app.static(
        "/testing.file",
        expected_path,
        host="www.example.com",
    )

    headers = {"Host": "www.example.com"}
    request, response = app.test_client.get("/testing.file", headers=headers)

    if file_name == 'nonexistent.file':
        assert response.status == 404
    else:
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name) if file_name else b''

    request, response = app.test_client.get("/testing.file")
    assert response.status == 404