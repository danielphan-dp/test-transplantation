import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', '', 'nonexistent.file'])
def test_get_file_path(app, file_name, static_file_directory):
    if file_name == 'nonexistent.file':
        with pytest.raises(FileNotFound):
            app.static(
                "/nonexistent.file",
                get_file_path(static_file_directory, file_name),
                use_content_range=True,
            )
    else:
        app.static(
            f"/{file_name}",
            get_file_path(static_file_directory, file_name),
            use_content_range=True,
        )

        request, response = app.test_client.head(f"/{file_name}")
        assert response.status == 200
        assert "Accept-Ranges" in response.headers
        assert "Content-Length" in response.headers
        assert int(response.headers["Content-Length"]) == len(
            get_file_content(static_file_directory, file_name)
        )

def test_get_file_path_empty_directory(app):
    static_file_directory = ''
    file_name = 'test.file'
    path = get_file_path(static_file_directory, file_name)
    assert path == os.path.join('', file_name)