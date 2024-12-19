import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

def test_get_file_path_valid_input():
    static_file_directory = "/valid/directory"
    file_name = "test.file"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_empty_directory():
    static_file_directory = ""
    file_name = "test.file"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_empty_file_name():
    static_file_directory = "/valid/directory"
    file_name = ""
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_none_directory():
    with pytest.raises(TypeError):
        get_file_path(None, "test.file")

def test_get_file_path_none_file_name():
    with pytest.raises(TypeError):
        get_file_path("/valid/directory", None)

def test_get_file_path_special_characters():
    static_file_directory = "/valid/directory"
    file_name = "test@file!.txt"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_long_file_name():
    static_file_directory = "/valid/directory"
    file_name = "a" * 255 + ".txt"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path