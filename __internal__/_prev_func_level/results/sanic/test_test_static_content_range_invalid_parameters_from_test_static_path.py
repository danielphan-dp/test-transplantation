import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt", "non_existent.file"])
def test_get_file_path(app, static_file_directory, file_name):
    if file_name == "non_existent.file":
        with pytest.raises(FileNotFound):
            get_file_path(static_file_directory, file_name)
    else:
        path = get_file_path(static_file_directory, file_name)
        assert os.path.exists(path)  # Check if the path exists for valid files
        assert path.startswith(static_file_directory)  # Ensure the path is within the static directory

@pytest.mark.parametrize("file_name", ["", "   ", None])
def test_get_file_path_invalid_names(app, static_file_directory, file_name):
    with pytest.raises(ValueError):
        get_file_path(static_file_directory, file_name)