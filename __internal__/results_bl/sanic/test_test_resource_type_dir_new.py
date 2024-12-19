import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

def test_get_file_path_valid(app, static_file_directory):
    file_name = "test.file"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_empty_directory(app):
    static_file_directory = ""
    file_name = "test.file"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_none_directory(app):
    with pytest.raises(TypeError):
        get_file_path(None, "test.file")

def test_get_file_path_invalid_file_name(app, static_file_directory):
    invalid_file_name = ""
    expected_path = os.path.join(static_file_directory, invalid_file_name)
    assert get_file_path(static_file_directory, invalid_file_name) == expected_path

def test_get_file_path_special_characters(app, static_file_directory):
    file_name = "test@file!.txt"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_long_file_name(app, static_file_directory):
    file_name = "a" * 255 + ".txt"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_with_pathlib(app, static_file_directory):
    from pathlib import Path
    file_name = "test.file"
    expected_path = Path(static_file_directory) / file_name
    assert get_file_path(static_file_directory, file_name) == str(expected_path)