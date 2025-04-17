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
    with pytest.raises(TypeError):
        get_file_path(None, "test.file")

def test_get_file_path_with_special_characters(static_file_directory):
    file_name = "decode me.txt"
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_static_file_not_found(app, static_file_directory):
    app.static("/static", static_file_directory, resource_type="dir")
    _, response = app.test_client.get("/static/non_existent.file")
    assert response.status == 404

def test_static_file_with_hard_link(app, static_file_directory):
    hard_link_name = "hard_link"
    src = os.path.abspath(os.path.join(os.path.dirname(static_file_directory), "conftest.py"))
    dist = os.path.join(static_file_directory, hard_link_name)
    os.link(src, dist)
    
    app.static("/testing.file", get_file_path(static_file_directory, hard_link_name))
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, hard_link_name)
    
    os.remove(dist)