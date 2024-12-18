import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
def test_static_file_path_not_found(app, static_file_directory, file_name):
    app = Sanic("base")
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        use_content_range=True,
    )

    uri = app.url_for("static")
    request, response = app.test_client.get(uri)
    assert response.status == 404

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_path_valid(app, static_file_directory, file_name):
    app = Sanic("base")
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        use_content_range=True,
    )

    uri = app.url_for("static")
    request, response = app.test_client.get(uri)
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_file_path_with_query_params(app, static_file_directory, file_name):
    app = Sanic("base")
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        use_content_range=True,
    )

    uri = app.url_for("static", filename=file_name)
    request, response = app.test_client.get(uri + '?param=value')
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)