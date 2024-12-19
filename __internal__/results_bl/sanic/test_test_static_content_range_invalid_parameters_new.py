import os
import pytest
from sanic import Sanic
from sanic.exceptions import ServerError

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', '', 'invalid/file/name.txt'])
def test_get_file_path(app, file_name, static_file_directory):
    if file_name == '':
        expected_path = os.path.join(static_file_directory, '')
    else:
        expected_path = os.path.join(static_file_directory, file_name)

    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_invalid_directory(app):
    with pytest.raises(ServerError):
        get_file_path(None, 'test.file')