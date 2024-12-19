import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
def test_get_file_path(app, static_file_directory, file_name):
    if file_name == 'non_existent.file':
        with pytest.raises(FileNotFound):
            get_file_path(static_file_directory, file_name)
    else:
        path = get_file_path(static_file_directory, file_name)
        assert os.path.join(static_file_directory, file_name) == path

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_file_path_with_valid_files(app, static_file_directory, file_name):
    path = get_file_path(static_file_directory, file_name)
    app.static("/testing.file", path)
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)