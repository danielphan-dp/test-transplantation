import os
import pytest
from sanic import Sanic
from sanic.response import json

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt", "non_existent.file"])
@pytest.mark.parametrize("static_file_directory", ["./static", "./another_static"])
def test_get_file_path(app, file_name, static_file_directory):
    if file_name == "non_existent.file":
        with pytest.raises(FileNotFoundError):
            get_file_path(static_file_directory, file_name)
    else:
        file_path = get_file_path(static_file_directory, file_name)
        assert os.path.join(static_file_directory, file_name) == file_path

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt"])
def test_static_file_with_valid_files(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert "Content-Length" in response.headers
    assert response.body == bytes(get_file_content(static_file_directory, file_name))

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt"])
def test_static_file_with_invalid_directory(app, file_name):
    invalid_directory = "./invalid_static"
    app.static("/testing.file", get_file_path(invalid_directory, file_name))
    request, response = app.test_client.get("/testing.file")
    assert response.status == 404

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt"])
def test_static_file_with_empty_file_name(app, static_file_directory):
    empty_file_name = ""
    app.static("/testing.file", get_file_path(static_file_directory, empty_file_name))
    request, response = app.test_client.get("/testing.file")
    assert response.status == 404