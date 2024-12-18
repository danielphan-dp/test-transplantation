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
def test_static_file_with_different_paths(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))
    app.static("/another_path/testing.file", get_file_path(static_file_directory, file_name))

    request, response = app.test_client.get("/another_path/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_content_length(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert 'Content-Length' in response.headers
    assert response.headers['Content-Length'] == str(len(get_file_content(static_file_directory, file_name)))