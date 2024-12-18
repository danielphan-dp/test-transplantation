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
def test_static_file_with_invalid_range(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    headers = {"Range": "bytes=999-1000"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    assert response.status == 416  # Range Not Satisfiable

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_with_empty_range(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    headers = {"Range": "bytes=0-0"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    static_content = bytes(get_file_content(static_file_directory, file_name))[:1]
    assert response.status == 206
    assert int(response.headers["Content-Length"]) == len(static_content)
    assert response.body == static_content

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_with_full_range(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    headers = {"Range": "bytes=0-"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    static_content = bytes(get_file_content(static_file_directory, file_name))
    assert response.status == 206
    assert int(response.headers["Content-Length"]) == len(static_content)
    assert response.body == static_content

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_with_partial_range(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    headers = {"Range": "bytes=5-10"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    static_content = bytes(get_file_content(static_file_directory, file_name))[5:11]
    assert response.status == 206
    assert int(response.headers["Content-Length"]) == len(static_content)
    assert response.body == static_content