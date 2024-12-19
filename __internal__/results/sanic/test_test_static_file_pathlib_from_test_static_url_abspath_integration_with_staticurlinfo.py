import os
import pytest
from pathlib import Path
from sanic import Sanic

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png', 'symlink', 'hard_link', 'non_existent.file'])
def test_static_file_with_non_existent(app, static_file_directory, file_name):
    if file_name == 'non_existent.file':
        with pytest.raises(FileNotFoundError):
            app.static("/testing.file", get_file_path(static_file_directory, file_name))
            request, response = app.test_client.get("/testing.file")
    else:
        app.static("/testing.file", get_file_path(static_file_directory, file_name))
        request, response = app.test_client.get("/testing.file")
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png', 'symlink', 'hard_link'])
def test_static_file_with_pathlib(app, static_file_directory, file_name):
    file_path = Path(get_file_path(static_file_directory, file_name))
    app.static("/testing.file", file_path)
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png', 'symlink', 'hard_link'])
def test_static_file_with_absolute_path(app, static_file_directory, file_name):
    absolute_path = os.path.abspath(get_file_path(static_file_directory, file_name))
    app.static("/testing.file", absolute_path)
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)