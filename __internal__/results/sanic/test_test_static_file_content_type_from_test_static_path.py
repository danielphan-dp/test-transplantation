import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize("file_name", ["non_existent_file.txt", "", "valid_file.txt"])
def test_get_file_path(app, static_file_directory, file_name):
    if file_name == "non_existent_file.txt":
        with pytest.raises(FileNotFound):
            app.static("/testing.file", get_file_path(static_file_directory, file_name))
            request, response = app.test_client.get("/testing.file")
    elif file_name == "":
        with pytest.raises(ValueError):
            app.static("/testing.file", get_file_path(static_file_directory, file_name))
    else:
        app.static("/testing.file", get_file_path(static_file_directory, file_name))
        request, response = app.test_client.get("/testing.file")
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name)
        assert response.headers["Content-Type"] == "text/html; charset=utf-8"