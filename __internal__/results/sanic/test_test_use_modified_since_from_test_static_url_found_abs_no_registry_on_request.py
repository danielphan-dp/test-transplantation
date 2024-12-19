import os
import pytest
from sanic import Sanic
from time import gmtime, strftime

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png', 'non_existent.file'])
def test_get_file_path(app, static_file_directory, file_name):
    if file_name == 'non_existent.file':
        with pytest.raises(FileNotFoundError):
            app.static("/testing.file", get_file_path(static_file_directory, file_name))
            request, response = app.test_client.get("/testing.file")
    else:
        app.static("/testing.file", get_file_path(static_file_directory, file_name))
        request, response = app.test_client.get("/testing.file")
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png'])
def test_get_file_path_with_modified_since(app, static_file_directory, file_name):
    file_stat = os.stat(get_file_path(static_file_directory, file_name))
    modified_since = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime(file_stat.st_mtime))

    app.static("/testing.file", get_file_path(static_file_directory, file_name), use_modified_since=True)

    request, response = app.test_client.get("/testing.file", headers={"If-Modified-Since": modified_since})
    assert response.status == 304

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png'])
def test_get_file_path_with_different_headers(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    request, response = app.test_client.get("/testing.file", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)