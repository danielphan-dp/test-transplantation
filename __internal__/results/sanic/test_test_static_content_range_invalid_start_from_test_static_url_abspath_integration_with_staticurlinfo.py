import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
def test_get_file_path(app, file_name, static_file_directory):
    if file_name == 'non_existent.file':
        with pytest.raises(FileNotFound):
            get_file_path(static_file_directory, file_name)
    else:
        path = get_file_path(static_file_directory, file_name)
        assert os.path.join(static_file_directory, file_name) == path

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_file_path_with_valid_files(app, file_name, static_file_directory):
    path = get_file_path(static_file_directory, file_name)
    assert os.path.exists(path)  # Ensure the file exists in the static directory

def test_get_file_path_invalid_directory(app):
    invalid_directory = "/invalid/static/directory"
    file_name = "test.file"
    with pytest.raises(FileNotFound):
        get_file_path(invalid_directory, file_name)