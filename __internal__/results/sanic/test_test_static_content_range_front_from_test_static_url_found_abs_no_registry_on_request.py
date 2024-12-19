import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize("file_name", ["non_existent.file", "invalid_path/../test.file"])
def test_get_file_path_invalid(app, static_file_directory, file_name):
    with pytest.raises(FileNotFound):
        app.static("/testing.file", get_file_path(static_file_directory, file_name))

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt"])
def test_get_file_path_valid(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt"])
def test_get_file_path_content_range(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name), use_content_range=True)
    headers = {"Range": "bytes=0-9"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    assert response.status == 206
    assert "Content-Length" in response.headers
    assert "Content-Range" in response.headers
    static_content = bytes(get_file_content(static_file_directory, file_name))[:10]
    assert int(response.headers["Content-Length"]) == len(static_content)
    assert response.body == static_content

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt"])
def test_get_file_path_edge_cases(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)
    assert response.headers["Content-Type"] == "application/octet-stream"  # Assuming default content type for static files