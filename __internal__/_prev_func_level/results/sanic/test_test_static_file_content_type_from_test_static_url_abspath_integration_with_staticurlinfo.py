import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize("file_name", ["non_existent_file.txt", "another_test.file"])
def test_get_file_path_invalid_files(app, static_file_directory, file_name):
    with pytest.raises(FileNotFound):
        app.static("/testing.file", get_file_path(static_file_directory, file_name))
        request, response = app.test_client.get("/testing.file")
        assert response.status == 404

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt", "python.png"])
def test_get_file_path_valid_files(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

def test_get_file_path_edge_case(app, static_file_directory):
    file_name = "test.html"
    app.static("/testing.file", get_file_path(static_file_directory, file_name), content_type="text/html; charset=utf-8")
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"