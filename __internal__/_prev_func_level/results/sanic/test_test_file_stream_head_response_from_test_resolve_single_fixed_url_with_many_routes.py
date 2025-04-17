import os
import pytest
from sanic import Sanic
from sanic.response import text, HTTPResponse
from urllib.parse import unquote

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
async def test_file_stream_head_response(app: Sanic, file_name, static_file_directory):
    @app.route("/files/<filename>", methods=["GET", "HEAD"])
    async def file_route(request, filename):
        file_path = os.path.join(static_file_directory, filename)
        file_path = os.path.abspath(unquote(file_path))
        headers = {}
        headers["Accept-Ranges"] = "bytes"
        if request.method == "HEAD":
            if not os.path.exists(file_path):
                return HTTPResponse(status=404)
            stats = await async_os.stat(file_path)
            headers["Content-Length"] = str(stats.st_size)
            return HTTPResponse(
                headers=headers,
                content_type=guess_type(file_path)[0] or "text/plain",
            )
        else:
            return file_stream(
                file_path,
                chunk_size=32,
                headers=headers,
                mime_type=guess_type(file_path)[0] or "text/plain",
            )

    request, response = app.test_client.head(f"/files/{file_name}")
    
    if file_name == 'non_existent.file':
        assert response.status == 404
    else:
        assert response.status == 200
        assert "Accept-Ranges" in response.headers
        assert "Content-Length" in response.headers
        assert int(response.headers["Content-Length"]) == len(
            get_file_content(static_file_directory, file_name)
        )
        if "Transfer-Encoding" in response.headers:
            assert response.headers["Transfer-Encoding"] != "chunked"