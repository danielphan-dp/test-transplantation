import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
@pytest.mark.parametrize('static_file_directory', ['./static', './invalid_directory'])
def test_get_file_path(app, file_name, static_file_directory):
    if static_file_directory == './invalid_directory':
        with pytest.raises(FileNotFound):
            get_file_path(static_file_directory, file_name)
    else:
        file_path = get_file_path(static_file_directory, file_name)
        assert os.path.join(static_file_directory, file_name) == file_path
        assert os.path.exists(file_path) == (file_name in os.listdir(static_file_directory))