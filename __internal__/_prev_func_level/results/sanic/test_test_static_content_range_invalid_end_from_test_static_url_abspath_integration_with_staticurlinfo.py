import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
def test_get_file_path(app, static_file_directory, file_name):
    if file_name == 'non_existent.file':
        with pytest.raises(FileNotFound):
            get_file_path(static_file_directory, file_name)
    else:
        path = get_file_path(static_file_directory, file_name)
        assert os.path.exists(path)  # Ensure the file path exists for valid files
        assert path == os.path.join(static_file_directory, file_name)  # Check the constructed path is correct

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_get_file_path_with_invalid_directory(app, static_file_directory, file_name):
    invalid_directory = "/invalid/directory"
    path = get_file_path(invalid_directory, file_name)
    assert not os.path.exists(path)  # Ensure the path does not exist for invalid directory

def test_get_file_path_edge_cases(app, static_file_directory):
    edge_case_file_name = ""
    path = get_file_path(static_file_directory, edge_case_file_name)
    assert path == os.path.join(static_file_directory, edge_case_file_name)  # Check handling of empty file name

    edge_case_file_name = " "  # Space as file name
    path = get_file_path(static_file_directory, edge_case_file_name)
    assert path == os.path.join(static_file_directory, edge_case_file_name)  # Check handling of space as file name