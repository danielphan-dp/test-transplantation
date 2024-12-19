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

def test_static_file_with_invalid_path(app, static_file_directory):
    invalid_file_name = "non_existent.file"
    app.static("/static", static_file_directory, resource_type="dir")
    
    _, response = app.test_client.get(f"/static/{invalid_file_name}")
    assert response.status == 404

def test_static_file_with_valid_path(app, static_file_directory):
    valid_file_name = "test.file"
    app.static("/static", static_file_directory, resource_type="dir")
    
    _, response = app.test_client.get(f"/static/{valid_file_name}")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, valid_file_name)