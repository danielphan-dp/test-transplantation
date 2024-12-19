import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.fixture
def static_file_directory():
    current_file = inspect.getfile(inspect.currentframe())
    current_directory = os.path.dirname(os.path.abspath(current_file))
    static_directory = os.path.join(current_directory, "static")
    return static_directory

def test_get_file_path_valid(static_file_directory):
    file_name = "test.file"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_invalid(static_file_directory):
    file_name = "non_existent.file"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_static_file_not_found(app, static_file_directory):
    app.static("/missing", get_file_path(static_file_directory, "missing.file"))
    _, response = app.test_client.get("/missing")
    assert response.status == 404

def test_static_file_with_special_characters(app, static_file_directory):
    file_name = "decode me.txt"
    app.static("/decode", get_file_path(static_file_directory, file_name))
    _, response = app.test_client.get("/decode")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

def test_static_file_with_symlink(app, static_file_directory):
    symlink_name = "symlink"
    os.symlink(os.path.join(static_file_directory, "test.file"), os.path.join(static_file_directory, symlink_name))
    app.static("/symlink", get_file_path(static_file_directory, symlink_name))
    _, response = app.test_client.get("/symlink")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, "test.file")