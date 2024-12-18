import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
def test_static_file_path_not_found(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    request, response = app.test_client.get("/testing.file")
    if file_name == 'non_existent.file':
        assert response.status == 404
    else:
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_content_range_incorrect(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name), use_content_range=True)

    headers = {"Range": "bytes=100-200"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    assert response.status == 416  # Range Not Satisfiable

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_content_range_boundary(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name), use_content_range=True)

    headers = {"Range": "bytes=0-5"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    static_content = bytes(get_file_content(static_file_directory, file_name))[:6]
    assert response.status == 206
    assert "Content-Length" in response.headers
    assert "Content-Range" in response.headers
    assert int(response.headers["Content-Length"]) == len(static_content)
    assert response.body == static_content

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_with_different_directory(app, static_file_directory, file_name):
    different_directory = os.path.join(static_file_directory, 'subdir')
    app.static("/testing.file", get_file_path(different_directory, file_name))

    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(different_directory, file_name)