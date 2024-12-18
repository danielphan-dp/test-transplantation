import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
def test_static_file_path_not_found(app, file_name, static_file_directory):
    app = Sanic("base")
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    request, response = app.test_client.get("/testing.file")
    if file_name == 'non_existent.file':
        assert response.status == 404
    else:
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_with_invalid_range(app, file_name, static_file_directory):
    app = Sanic("base")
    app.static("/testing.file", get_file_path(static_file_directory, file_name), use_content_range=True)

    headers = {"Range": "bytes=100-200"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    assert response.status == 416
    assert "Content-Length" in response.headers
    assert "Content-Range" in response.headers
    assert response.headers["Content-Range"] == "bytes */%s" % (len(get_file_content(static_file_directory, file_name)),)

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_with_valid_range(app, file_name, static_file_directory):
    app = Sanic("base")
    app.static("/testing.file", get_file_path(static_file_directory, file_name), use_content_range=True)

    headers = {"Range": "bytes=0-10"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    assert response.status == 206
    assert "Content-Length" in response.headers
    assert "Content-Range" in response.headers
    assert response.headers["Content-Range"].startswith("bytes 0-10/")