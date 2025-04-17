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
        file_path = get_file_path(static_file_directory, file_name)
        assert os.path.exists(file_path)  # Ensure the file path exists for valid files
        assert file_path == os.path.join(static_file_directory, file_name)  # Check the constructed path

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_file_path_with_invalid_directory(app, file_name):
    invalid_directory = "/invalid/static/directory"
    file_path = get_file_path(invalid_directory, file_name)
    assert not os.path.exists(file_path)  # Ensure the path does not exist for invalid directory