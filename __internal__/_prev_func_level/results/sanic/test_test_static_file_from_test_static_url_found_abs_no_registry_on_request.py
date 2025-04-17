import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize("file_name", ["non_existent.file", "invalid_path/../file.txt"])
def test_static_file_not_found(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    request, response = app.test_client.get("/testing.file")
    assert response.status == 404

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt", "python.png", "symlink", "hard_link"])
def test_static_file_with_different_names(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt", "python.png", "symlink", "hard_link"])
def test_static_file_pathlib(app, static_file_directory, file_name):
    from pathlib import Path
    file_path = Path(get_file_path(static_file_directory, file_name))
    app.static("/testing.file", file_path)

    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)