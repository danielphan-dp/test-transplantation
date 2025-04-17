import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize(
    "file_name,expected",
    [
        ("test.html", "text/html; charset=utf-8"),
        ("decode me.txt", "text/plain; charset=utf-8"),
        ("test.file", "application/octet-stream"),
        ("non_existent.file", FileNotFound),
        ("", FileNotFound)
    ]
)
def test_get_file_path(app, static_file_directory, file_name, expected):
    if expected is FileNotFound:
        with pytest.raises(FileNotFound):
            get_file_path(static_file_directory, file_name)
    else:
        app.static(
            "/testing.file",
            get_file_path(static_file_directory, file_name),
        )

        request, response = app.test_client.get("/testing.file")
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name)
        assert response.headers["Content-Type"] == expected