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

def test_get_file_path_empty_file_name(static_file_directory):
    file_name = ""
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_invalid_directory():
    with pytest.raises(FileNotFound):
        get_file_path("/invalid/directory", "test.file")

def test_get_file_path_with_special_characters(static_file_directory):
    file_name = "decode me.txt"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_with_symlink(static_file_directory):
    file_name = "symlink"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_hard_link(static_file_directory):
    file_name = "hard_link"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_multiple_statics(app, static_file_directory):
    app.static("/file", get_file_path(static_file_directory, "test.file"), name="file")
    app.static("/png", get_file_path(static_file_directory, "python.png"), name="png")

    _, response = app.test_client.get("/file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, "test.file")

    _, response = app.test_client.get("/png")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, "python.png")