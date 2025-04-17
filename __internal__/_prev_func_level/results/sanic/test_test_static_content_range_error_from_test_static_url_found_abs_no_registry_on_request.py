import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize("file_name", ["non_existent.file", "invalid_path/../test.file"])
def test_get_file_path_invalid(app, file_name, static_file_directory):
    with pytest.raises(FileNotFound):
        app.static("/testing.file", get_file_path(static_file_directory, file_name))
        request, response = app.test_client.get("/testing.file")
        assert response.status == 404

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt"])
def test_get_file_path_valid(app, file_name, static_file_directory):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt"])
def test_get_file_path_content_range(app, file_name, static_file_directory):
    app.static("/testing.file", get_file_path(static_file_directory, file_name), use_content_range=True)
    headers = {"Range": "bytes=0-5"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    assert response.status == 206
    assert "Content-Range" in response.headers
    assert response.headers["Content-Range"].startswith("bytes 0-5/")