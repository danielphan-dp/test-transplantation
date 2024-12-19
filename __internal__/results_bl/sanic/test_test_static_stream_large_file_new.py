import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['test.file', 'large.file', '', 'non_existent.file'])
def test_get_file_path(static_file_directory, file_name):
    if file_name == '':
        expected_path = os.path.join(static_file_directory, '')
    else:
        expected_path = os.path.join(static_file_directory, file_name)

    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_invalid_directory():
    with pytest.raises(FileNotFound):
        get_file_path('/invalid/directory', 'file.txt')