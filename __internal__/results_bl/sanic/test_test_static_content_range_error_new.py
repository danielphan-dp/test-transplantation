import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound, ServerError

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', '', 'nonexistent.file'])
def test_get_file_path(app, file_name, static_file_directory):
    if file_name == 'nonexistent.file':
        with pytest.raises(FileNotFound):
            get_file_path(static_file_directory, file_name)
    else:
        path = get_file_path(static_file_directory, file_name)
        assert os.path.join(static_file_directory, file_name) == path

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_content_valid_file(app, file_name, static_file_directory):
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        use_content_range=True,
    )

    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert "Content-Length" in response.headers
    assert "Content-Range" in response.headers

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_content_empty_file(app, file_name, static_file_directory):
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        use_content_range=True,
    )

    headers = {"Range": "bytes=0-0"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    assert response.status == 206
    assert response.headers["Content-Range"] == "bytes 0-0/%s" % (
        len(get_file_content(static_file_directory, file_name)),
    )