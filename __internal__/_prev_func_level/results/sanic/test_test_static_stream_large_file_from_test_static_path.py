import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['non_existent.file', 'test.file'])
def test_static_file_path_not_found(app, static_file_directory, file_name):
    if file_name == 'non_existent.file':
        with pytest.raises(FileNotFound):
            app.static("/testing.file", get_file_path(static_file_directory, file_name))
            request, response = app.test_client.get("/testing.file")
    else:
        app.static("/testing.file", get_file_path(static_file_directory, file_name))
        request, response = app.test_client.get("/testing.file")
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize('file_name', ['test.file', 'large.file'])
@pytest.mark.parametrize('use_modified_since', [True, False])
def test_static_file_with_modified_since(app, static_file_directory, file_name, use_modified_since):
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        use_modified_since=use_modified_since
    )
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize('file_name', ['test.file', 'large.file'])
@pytest.mark.parametrize('stream_large_files', [True, 1024])
def test_static_file_stream_large_files(app, static_file_directory, file_name, stream_large_files):
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        stream_large_files=stream_large_files
    )
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)