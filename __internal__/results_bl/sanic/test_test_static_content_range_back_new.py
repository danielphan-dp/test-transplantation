import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', '', 'nonexistent.file'])
def test_get_file_path(app, file_name, static_file_directory):
    if file_name == 'nonexistent.file':
        with pytest.raises(FileNotFound):
            get_file_path(static_file_directory, file_name)
    else:
        path = get_file_path(static_file_directory, file_name)
        assert os.path.join(static_file_directory, file_name) == path

@pytest.mark.parametrize('static_file_directory, file_name', [
    ('/valid/path', 'test.file'),
    ('/another/valid/path', 'decode me.txt'),
    ('/invalid/path', 'nonexistent.file')
])
def test_get_file_path_with_valid_and_invalid_paths(app, static_file_directory, file_name):
    if file_name == 'nonexistent.file':
        with pytest.raises(FileNotFound):
            get_file_path(static_file_directory, file_name)
    else:
        path = get_file_path(static_file_directory, file_name)
        assert os.path.join(static_file_directory, file_name) == path

def test_get_file_path_empty_file_name(app, static_file_directory):
    path = get_file_path(static_file_directory, '')
    assert path == os.path.join(static_file_directory, '')