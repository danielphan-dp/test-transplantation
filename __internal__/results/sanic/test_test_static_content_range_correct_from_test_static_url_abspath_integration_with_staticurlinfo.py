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

    bp = Blueprint("test_bp_static", url_prefix="/bp")
    bp.static(
        "/testing.file",
        get_file_path(static_file_directory, file_name),
        use_content_range=True,
    )
    app.blueprint(bp)

    headers = {"Range": "bytes=0-10"}
    uri = app.url_for("static")
    
    if file_name == 'non_existent.file':
        request, response = app.test_client.get(uri, headers=headers)
        assert response.status == 404
    else:
        request, response = app.test_client.get(uri, headers=headers)
        assert response.status == 206
        assert "Content-Length" in response.headers
        assert "Content-Range" in response.headers
        static_content = bytes(get_file_content(static_file_directory, file_name))[
            0:11
        ]
        assert int(response.headers["Content-Length"]) == len(static_content)
        assert response.body == static_content

    uri = app.url_for("static", name="test_bp_static.static")
    if file_name == 'non_existent.file':
        request, response = app.test_client.get(uri, headers=headers)
        assert response.status == 404
    else:
        request, response = app.test_client.get(uri, headers=headers)
        assert response.status == 206
        assert "Content-Length" in response.headers
        assert "Content-Range" in response.headers
        static_content = bytes(get_file_content(static_file_directory, file_name))[
            0:11
        ]
        assert int(response.headers["Content-Length"]) == len(static_content)
        assert response.body == static_content