import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
def test_static_content_range_edge_cases(file_name, static_file_directory):
    app = Sanic("base")
    app.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        use_content_range=True,
    )

    request, response = app.test_client.get("/testing.file")
    
    if file_name == 'non_existent.file':
        assert response.status == 404
    else:
        assert response.status == 200
        assert "Content-Length" in response.headers
        assert "Content-Range" not in response.headers
        assert int(response.headers["Content-Length"]) == len(
            get_file_content(static_file_directory, file_name)
        )
        assert response.body == bytes(
            get_file_content(static_file_directory, file_name)
        )

    bp = Blueprint("test_bp_static", url_prefix="/bp")
    bp.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        use_content_range=True,
    )
    app.blueprint(bp)

    uri = app.url_for("test_bp_static.static")
    request, response = app.test_client.get(uri)
    
    if file_name == 'non_existent.file':
        assert response.status == 404
    else:
        assert response.status == 200
        assert "Content-Length" in response.headers
        assert "Content-Range" not in response.headers
        assert int(response.headers["Content-Length"]) == len(
            get_file_content(static_file_directory, file_name)
        )
        assert response.body == bytes(
            get_file_content(static_file_directory, file_name)
        )