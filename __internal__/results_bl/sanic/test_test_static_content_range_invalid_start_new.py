import os
import pytest
from sanic import Sanic
from sanic.exceptions import ServerError

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_file_path(app, file_name, static_file_directory):
    # Test valid file path
    valid_path = get_file_path(static_file_directory, file_name)
    assert os.path.exists(valid_path) == True

    # Test empty file name
    empty_file_name = ""
    empty_path = get_file_path(static_file_directory, empty_file_name)
    assert os.path.join(static_file_directory, empty_file_name) == empty_path

    # Test file name with special characters
    special_file_name = "test@file!.txt"
    special_path = get_file_path(static_file_directory, special_file_name)
    assert os.path.join(static_file_directory, special_file_name) == special_path

    # Test file name with leading/trailing spaces
    spaced_file_name = "  test.file  "
    spaced_path = get_file_path(static_file_directory, spaced_file_name.strip())
    assert os.path.join(static_file_directory, spaced_file_name.strip()) == spaced_path

    # Test non-existent file path
    non_existent_file_name = "non_existent.file"
    non_existent_path = get_file_path(static_file_directory, non_existent_file_name)
    assert os.path.exists(non_existent_path) == False

    # Test path traversal characters
    traversal_file_name = "../test.file"
    traversal_path = get_file_path(static_file_directory, traversal_file_name)
    assert os.path.join(static_file_directory, traversal_file_name) == traversal_path

    # Test long file name
    long_file_name = "a" * 255 + ".txt"
    long_path = get_file_path(static_file_directory, long_file_name)
    assert os.path.join(static_file_directory, long_file_name) == long_path

    # Test file name with unicode characters
    unicode_file_name = "测试文件.txt"
    unicode_path = get_file_path(static_file_directory, unicode_file_name)
    assert os.path.join(static_file_directory, unicode_file_name) == unicode_path