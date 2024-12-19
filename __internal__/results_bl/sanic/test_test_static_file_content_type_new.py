import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['test.html', '', 'non_existent_file.html'])
def test_get_file_path(app, static_file_directory, file_name):
    if file_name == '':
        expected_path = os.path.join(static_file_directory, '')
    else:
        expected_path = os.path.join(static_file_directory, file_name)

    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_invalid_directory(app):
    with pytest.raises(FileNotFound):
        get_file_path('/invalid/directory', 'test.html')