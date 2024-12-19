import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('static_file_directory,file_name,expected', [
    ('/valid/path', 'test.html', '/valid/path/test.html'),
    ('/another/valid/path', 'decode me.txt', '/another/valid/path/decode me.txt'),
    ('/yet/another/path', 'test.file', '/yet/another/path/test.file'),
    ('/empty/path', '', '/empty/path/'),
])
def test_get_file_path(static_file_directory, file_name, expected):
    assert get_file_path(static_file_directory, file_name) == expected

def test_get_file_path_invalid_directory():
    with pytest.raises(FileNotFound):
        get_file_path('/invalid/path', 'file.txt')