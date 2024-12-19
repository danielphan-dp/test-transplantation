import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', ''])
@pytest.mark.parametrize('static_file_directory', ['/valid/path', '/invalid/path'])
def test_get_file_path(file_name, static_file_directory):
    if static_file_directory == '/invalid/path' and file_name == '':
        with pytest.raises(FileNotFound):
            get_file_path(static_file_directory, file_name)
    else:
        result = get_file_path(static_file_directory, file_name)
        expected = os.path.join(static_file_directory, file_name)
        assert result == expected

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_file_path_with_special_characters(file_name):
    static_file_directory = '/valid/path'
    special_file_name = f"file_with_special_chars_@#!${file_name}"
    result = get_file_path(static_file_directory, special_file_name)
    expected = os.path.join(static_file_directory, special_file_name)
    assert result == expected

def test_get_file_path_empty_directory():
    file_name = 'test.file'
    static_file_directory = ''
    result = get_file_path(static_file_directory, file_name)
    expected = os.path.join(static_file_directory, file_name)
    assert result == expected

def test_get_file_path_none_file_name():
    static_file_directory = '/valid/path'
    file_name = None
    result = get_file_path(static_file_directory, file_name)
    expected = os.path.join(static_file_directory, '')
    assert result == expected