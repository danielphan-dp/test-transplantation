import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', '', 'nonexistent.file'])
def test_get_file_path(app, file_name, static_file_directory):
    if file_name == '':
        expected_path = os.path.join(static_file_directory, '')
        assert get_file_path(static_file_directory, file_name) == expected_path
    elif file_name == 'nonexistent.file':
        with pytest.raises(FileNotFound):
            get_file_path(static_file_directory, file_name)
    else:
        expected_path = os.path.join(static_file_directory, file_name)
        assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_with_special_characters(app, static_file_directory):
    file_name = 'file with spaces.txt'
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_with_long_filename(app, static_file_directory):
    file_name = 'a' * 255 + '.txt'
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path