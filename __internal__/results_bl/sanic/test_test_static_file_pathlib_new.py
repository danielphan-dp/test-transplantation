import os
import pytest
from pathlib import Path
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png', 'symlink', 'hard_link', '', None])
def test_get_file_path(app, static_file_directory, file_name):
    if file_name is None:
        with pytest.raises(TypeError):
            get_file_path(static_file_directory, file_name)
    else:
        file_path = get_file_path(static_file_directory, file_name)
        assert os.path.join(static_file_directory, file_name) == file_path
        if file_name == '':
            assert file_path == static_file_directory
        else:
            app.static("/testing.file", Path(file_path))
            request, response = app.test_client.get("/testing.file")
            if os.path.exists(file_path):
                assert response.status == 200
                assert response.body == get_file_content(static_file_directory, file_name)
            else:
                assert response.status == 404