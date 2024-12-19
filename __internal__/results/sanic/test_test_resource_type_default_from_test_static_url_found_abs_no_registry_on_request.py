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

@pytest.mark.parametrize(
    "file_name, expected_status",
    [
        ("test.file", 200),
        ("non_existent.file", 404),
        ("decode me.txt", 200),
        ("python.png", 200),
        ("symlink", 200),
        ("hard_link", 200),
    ],
)
def test_get_file_path(app, static_file_directory, file_name, expected_status):
    app.static("/file", get_file_path(static_file_directory, file_name), name="file")
    
    _, response = app.test_client.get("/file")
    assert response.status == expected_status
    
    if expected_status == 200:
        assert response.body == get_file_content(static_file_directory, file_name)