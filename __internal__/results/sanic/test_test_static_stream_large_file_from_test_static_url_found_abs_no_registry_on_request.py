import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['non_existent.file', ''])
def test_get_file_path_invalid(app, static_file_directory, file_name):
    with pytest.raises(FileNotFound):
        app.static("/testing.file", get_file_path(static_file_directory, file_name))
        request, response = app.test_client.get("/testing.file")
        assert response.status == 404

@pytest.mark.parametrize('file_name', ['test.file', 'large.file'])
def test_get_file_path_valid(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize('file_name', ['test.file', 'large.file'])
def test_get_file_path_with_trailing_slash(app, static_file_directory, file_name):
    app.static("/testing.file/", get_file_path(static_file_directory, file_name))
    request, response = app.test_client.get("/testing.file/")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize('file_name', ['test.file', 'large.file'])
def test_get_file_path_with_different_directory(app, static_file_directory, file_name):
    different_directory = os.path.join(static_file_directory, 'subdir')
    app.static("/testing.file", get_file_path(different_directory, file_name))
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(different_directory, file_name)