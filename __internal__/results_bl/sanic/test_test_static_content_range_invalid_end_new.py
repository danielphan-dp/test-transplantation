import os
import pytest

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_file_path(app, file_name, static_file_directory):
    # Test valid file path
    valid_path = get_file_path(static_file_directory, file_name)
    assert os.path.exists(valid_path) == True

    # Test with empty file name
    empty_file_name = ""
    empty_path = get_file_path(static_file_directory, empty_file_name)
    assert os.path.exists(empty_path) == False

    # Test with None as file name
    with pytest.raises(TypeError):
        get_file_path(static_file_directory, None)

    # Test with special characters in file name
    special_file_name = "test@file!.txt"
    special_path = get_file_path(static_file_directory, special_file_name)
    assert os.path.exists(special_path) == False

    # Test with long file name
    long_file_name = "a" * 260 + ".txt"
    long_path = get_file_path(static_file_directory, long_file_name)
    assert os.path.exists(long_path) == False