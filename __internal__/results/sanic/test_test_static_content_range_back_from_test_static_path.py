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
def test_static_file_path_with_different_directory(app, static_file_directory, file_name):
    new_directory = os.path.join(static_file_directory, 'subdir')
    os.makedirs(new_directory, exist_ok=True)
    app.static("/testing.file", get_file_path(new_directory, file_name))

    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(new_directory, file_name)

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_path_with_invalid_directory(app, static_file_directory, file_name):
    invalid_directory = os.path.join(static_file_directory, 'invalid_dir')
    app.static("/testing.file", get_file_path(invalid_directory, file_name))

    request, response = app.test_client.get("/testing.file")
    assert response.status == 404

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_path_with_large_file(app, static_file_directory, file_name):
    large_file_name = 'large_file.txt'
    app.static("/testing.file", get_file_path(static_file_directory, large_file_name))

    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, large_file_name)