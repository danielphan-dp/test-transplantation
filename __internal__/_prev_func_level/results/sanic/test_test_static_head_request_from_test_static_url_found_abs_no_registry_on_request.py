import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize("file_name", ["non_existent.file", "invalid_path/../test.file"])
def test_static_file_path_not_found(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    request, response = app.test_client.get("/testing.file")
    assert response.status == 404
    assert "File not found" in response.body.decode()

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt"])
def test_static_file_with_different_paths(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt"])
def test_static_file_head_request(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name), use_content_range=True)

    request, response = app.test_client.head("/testing.file")
    assert response.status == 200
    assert "Accept-Ranges" in response.headers
    assert "Content-Length" in response.headers
    assert int(response.headers["Content-Length"]) == len(get_file_content(static_file_directory, file_name))