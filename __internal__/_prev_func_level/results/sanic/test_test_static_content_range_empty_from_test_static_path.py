import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt", "non_existent.file"])
@pytest.mark.parametrize("static_file_directory", ["./static", "./another_static"])
def test_get_file_path(app, file_name, static_file_directory):
    if file_name == "non_existent.file":
        with pytest.raises(FileNotFound):
            get_file_path(static_file_directory, file_name)
    else:
        path = get_file_path(static_file_directory, file_name)
        assert os.path.join(static_file_directory, file_name) == path

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt"])
def test_get_file_path_with_different_directories(app, file_name):
    static_file_directory = "./static"
    path = get_file_path(static_file_directory, file_name)
    assert os.path.exists(path)  # Assuming the file exists in the static directory

    static_file_directory = "./another_static"
    path = get_file_path(static_file_directory, file_name)
    assert os.path.exists(path)  # Assuming the file exists in the another_static directory

def test_get_file_path_edge_cases(app):
    static_file_directory = "./static"
    file_name = ""
    path = get_file_path(static_file_directory, file_name)
    assert path == os.path.join(static_file_directory, "")

    file_name = "   "
    path = get_file_path(static_file_directory, file_name)
    assert path == os.path.join(static_file_directory, "   ")