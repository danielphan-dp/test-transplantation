import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize("file_name", ["non_existent.file", "another_test.file"])
def test_static_file_not_found(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))

    request, response = app.test_client.get("/testing.file")
    assert response.status == 404

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt", "python.png"])
def test_static_file_with_different_hosts(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name), host="www.example.com")

    headers = {"Host": "www.example.com"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

    headers = {"Host": "www.anotherexample.com"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    assert response.status == 404

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt", "python.png"])
def test_static_file_pathlib_with_invalid_path(app, static_file_directory, file_name):
    from pathlib import Path
    invalid_path = Path(static_file_directory) / "invalid_directory" / file_name
    app.static("/testing.file", invalid_path)

    request, response = app.test_client.get("/testing.file")
    assert response.status == 404

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt", "python.png"])
def test_static_file_with_symlink(app, static_file_directory, file_name):
    src = os.path.join(static_file_directory, file_name)
    symlink_path = os.path.join(static_file_directory, "symlink")
    os.symlink(src, symlink_path)

    app.static("/testing.file", symlink_path)
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

    os.remove(symlink_path)