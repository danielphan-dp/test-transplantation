import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

def test_get_file_path_valid(app, static_file_directory):
    file_name = "valid.file"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_empty_file_name(app, static_file_directory):
    file_name = ""
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_none_file_name(app, static_file_directory):
    with pytest.raises(TypeError):
        get_file_path(static_file_directory, None)

def test_get_file_path_invalid_directory(app):
    invalid_directory = "/invalid/directory"
    file_name = "test.file"
    with pytest.raises(FileNotFound):
        get_file_path(invalid_directory, file_name)