import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
def test_static_head_request_with_non_existent_file(file_name, static_file_directory):
    app = Sanic("base")
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        use_content_range=True,
    )

    request, response = app.test_client.head("/testing.file")
    if file_name == 'non_existent.file':
        assert response.status == 404
    else:
        assert response.status == 200
        assert "Accept-Ranges" in response.headers
        assert "Content-Length" in response.headers
        assert int(response.headers["Content-Length"]) == len(
            get_file_content(static_file_directory, file_name)
        )

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_head_request_with_different_file_names(file_name, static_file_directory):
    app = Sanic("base")
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        use_content_range=True,
    )

    request, response = app.test_client.head("/testing.file")
    assert response.status == 200
    assert "Accept-Ranges" in response.headers
    assert "Content-Length" in response.headers
    assert int(response.headers["Content-Length"]) == len(
        get_file_content(static_file_directory, file_name)
    )

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_static_head_request_with_blueprint(file_name, static_file_directory):
    app = Sanic("base")
    bp = Blueprint("test_bp_static", url_prefix="/bp")
    bp.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        use_content_range=True,
    )
    app.blueprint(bp)

    request, response = app.test_client.head("/bp/testing.file")
    assert response.status == 200
    assert "Accept-Ranges" in response.headers
    assert "Content-Length" in response.headers
    assert int(response.headers["Content-Length"]) == len(
        get_file_content(static_file_directory, file_name)
    )