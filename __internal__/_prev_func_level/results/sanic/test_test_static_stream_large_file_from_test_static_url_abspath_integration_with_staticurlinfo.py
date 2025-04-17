import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['non_existent.file', 'test.file'])
def test_get_file_path(app, static_file_directory, file_name):
    if file_name == 'non_existent.file':
        with pytest.raises(FileNotFound):
            app.static("/testing.file", get_file_path(static_file_directory, file_name))
            request, response = app.test_client.get("/testing.file")
    else:
        app.static("/testing.file", get_file_path(static_file_directory, file_name))
        request, response = app.test_client.get("/testing.file")
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize('file_name', ['test.file', 'large.file'])
def test_get_file_path_with_special_characters(app, static_file_directory, file_name):
    special_file_name = f"test file with spaces and @chars/{file_name}"
    app.static("/testing.file", get_file_path(static_file_directory, special_file_name))
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, special_file_name)