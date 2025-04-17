import os
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
async def test_file_head_response(app: Sanic, file_name, static_file_directory):
    @app.route("/files/<filename>", methods=["HEAD"])
    async def file_route(request, filename):
        file_path = os.path.join(static_file_directory, filename)
        file_path = os.path.abspath(unquote(file_path))
        if not os.path.exists(file_path):
            return text('', status=404)
        stats = await async_os.stat(file_path)
        headers = {
            "Accept-Ranges": "bytes",
            "Content-Length": str(stats.st_size)
        }
        return HTTPResponse(headers=headers, content_type=guess_type(file_path)[0] or "text/plain")

    request, response = await app.test_client.head(f"/files/{file_name}")
    
    if file_name == 'non_existent.file':
        assert response.status == 404
    else:
        assert response.status == 200
        assert "Accept-Ranges" in response.headers
        assert "Content-Length" in response.headers
        assert int(response.headers["Content-Length"]) == len(get_file_content(static_file_directory, file_name))