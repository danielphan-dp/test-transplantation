import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['non_existent.file', 'invalid_path/../test.file'])
def test_static_file_invalid_cases(app, static_file_directory, file_name):
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        host="www.example.com",
    )

    headers = {"Host": "www.example.com"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    assert response.status == 404

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png'])
def test_static_file_with_different_hosts(app, static_file_directory, file_name):
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        host="www.example.com",
    )

    headers = {"Host": "www.example.com"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

    headers = {"Host": "www.anotherexample.com"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    assert response.status == 404

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png'])
def test_static_file_pathlib_with_invalid_file(app, static_file_directory, file_name):
    file_path = Path(get_file_path(static_file_directory, file_name))
    app.static("/testing.file", file_path)

    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

    invalid_file_path = Path(get_file_path(static_file_directory, 'invalid.file'))
    app.static("/invalid.file", invalid_file_path)
    request, response = app.test_client.get("/invalid.file")
    assert response.status == 404