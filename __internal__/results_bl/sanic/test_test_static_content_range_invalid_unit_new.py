import os
import pytest
from sanic import Sanic
from sanic.exceptions import ServerError

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', '', 'invalid/file/name'])
def test_get_file_path(static_file_directory, file_name):
    if file_name == '':
        expected = os.path.join(static_file_directory, '')
    elif 'invalid' in file_name:
        with pytest.raises(ServerError):
            get_file_path(static_file_directory, file_name)
        return
    else:
        expected = os.path.join(static_file_directory, file_name)

    assert get_file_path(static_file_directory, file_name) == expected

@pytest.mark.parametrize('static_file_directory, file_name', [
    ('/valid/path', 'file.txt'),
    ('/another/valid/path', 'another_file.txt'),
])
def test_get_file_path_valid(static_file_directory, file_name):
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

@pytest.mark.parametrize('static_file_directory, file_name', [
    ('/valid/path', 'file.txt'),
    ('/another/valid/path', 'another_file.txt'),
])
def test_get_file_path_edge_cases(static_file_directory, file_name):
    assert get_file_path(static_file_directory, file_name) != ''
    assert os.path.isabs(get_file_path(static_file_directory, file_name)) == False