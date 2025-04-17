import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize("file_name", ["valid_file.txt", "another_file.txt", "non_existent_file.txt"])
def test_get_file_path(app, static_file_directory, file_name):
    if file_name == "non_existent_file.txt":
        with pytest.raises(FileNotFound):
            get_file_path(static_file_directory, file_name)
    else:
        file_path = get_file_path(static_file_directory, file_name)
        assert os.path.exists(file_path)
        assert os.path.isfile(file_path)