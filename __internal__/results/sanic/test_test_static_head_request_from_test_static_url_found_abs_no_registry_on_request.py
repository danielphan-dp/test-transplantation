import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
def test_static_file_not_found(app, static_file_directory, file_name):
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        use_content_range=True,
    )

    request, response = app.test_client.head("/testing.file")
    assert response.status == 404

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_with_invalid_directory(app, static_file_directory, file_name):
    invalid_directory = "/invalid/path"
    app.static(
        "/testing.file",
        get_file_path(invalid_directory, file_name),
        use_content_range=True,
    )

    request, response = app.test_client.head("/testing.file")
    assert response.status == 404

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_with_empty_filename(app, static_file_directory, file_name):
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, ''),
        use_content_range=True,
    )

    request, response = app.test_client.head("/testing.file")
    assert response.status == 404

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_with_special_characters(app, static_file_directory, file_name):
    special_file_name = "test@file!.txt"
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, special_file_name),
        use_content_range=True,
    )

    request, response = app.test_client.head("/testing.file")
    assert response.status == 404

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_with_large_file(app, static_file_directory, file_name):
    large_file_name = "large_file.txt"  # Assume this file exists and is large
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, large_file_name),
        use_content_range=True,
    )

    request, response = app.test_client.head("/testing.file")
    assert response.status == 200
    assert "Accept-Ranges" in response.headers
    assert "Content-Length" in response.headers
    assert int(response.headers["Content-Length"]) > 0  # Ensure it's a large file

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_with_symlink(app, static_file_directory, file_name):
    symlink_name = "symlink_to_test.file"  # Assume this symlink exists
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, symlink_name),
        use_content_range=True,
    )

    request, response = app.test_client.head("/testing.file")
    assert response.status == 200
    assert "Accept-Ranges" in response.headers
    assert "Content-Length" in response.headers
    assert int(response.headers["Content-Length"]) == len(
        get_file_content(static_file_directory, file_name)
    )