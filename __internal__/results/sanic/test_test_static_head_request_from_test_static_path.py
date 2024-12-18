import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
def test_static_file_path_not_found(app, static_file_directory, file_name):
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        use_content_range=True,
    )

    request, response = app.test_client.head("/testing.file")
    assert response.status == 404

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_path_with_different_directory(app, static_file_directory, file_name):
    new_static_directory = os.path.join(static_file_directory, 'new_static')
    os.makedirs(new_static_directory, exist_ok=True)

    app.static(
        "/new_testing.file",
        get_file_path(new_static_directory, file_name),
        use_content_range=True,
    )

    request, response = app.test_client.head("/new_testing.file")
    assert response.status == 404

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_path_with_symlink(app, static_file_directory, file_name):
    symlink_name = 'symlink'
    os.symlink(get_file_path(static_file_directory, file_name), os.path.join(static_file_directory, symlink_name))

    app.static(
        "/testing.file",
        get_file_path(static_file_directory, symlink_name),
        use_content_range=True,
    )

    request, response = app.test_client.head("/testing.file")
    assert response.status == 200
    assert "Accept-Ranges" in response.headers
    assert "Content-Length" in response.headers
    assert int(response.headers["Content-Length"]) == len(get_file_content(static_file_directory, file_name))

    os.remove(os.path.join(static_file_directory, symlink_name))