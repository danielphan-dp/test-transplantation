import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
def test_static_file_path_not_found(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    request, response = app.test_client.get("/testing.file")
    if file_name == 'non_existent.file':
        assert response.status == 404
    else:
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_path_with_invalid_range(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    headers = {"Range": "bytes=100-200"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    assert response.status == 416  # Range Not Satisfiable

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_path_with_empty_file(app, static_file_directory, file_name):
    empty_file_path = os.path.join(static_file_directory, 'empty.file')
    with open(empty_file_path, 'w') as f:
        pass  # Create an empty file

    app.static("/testing.file", get_file_path(static_file_directory, 'empty.file'))

    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == b''  # Expect empty response body

    os.remove(empty_file_path)  # Clean up the empty file after test