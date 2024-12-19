import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png', '', 'non_existent_file.txt'])
def test_get_file_path(app, static_file_directory, file_name):
    if file_name == 'non_existent_file.txt':
        with pytest.raises(FileNotFound):
            app.static("/non_existent.file", get_file_path(static_file_directory, file_name))
            app.test_client.get("/non_existent.file")
    else:
        file_path = get_file_path(static_file_directory, file_name)
        assert os.path.join(static_file_directory, file_name) == file_path
        app.static("/testing.file", file_path)
        request, response = app.test_client.get("/testing.file")
        assert response.status == 200

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png'])
def test_get_file_path_with_empty_string(app, static_file_directory, file_name):
    file_path = get_file_path(static_file_directory, '')
    assert os.path.join(static_file_directory, '') == file_path
    app.static("/empty.file", file_path)
    request, response = app.test_client.get("/empty.file")
    assert response.status == 200