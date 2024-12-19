import os
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['non_existent.file', 'empty.file'])
def test_head_response_for_non_existent_and_empty_files(app: Sanic, file_name, static_file_directory):
    @app.route("/files/<filename>", methods=["HEAD"])
    async def file_route(request, filename):
        file_path = os.path.join(static_file_directory, filename)
        file_path = os.path.abspath(unquote(file_path))
        if not os.path.exists(file_path):
            return text('', status=404)
        if os.path.getsize(file_path) == 0:
            return text('', headers={'Content-Length': '0'})
        return text('', headers={'Content-Length': str(os.path.getsize(file_path))})

    request, response = app.test_client.head(f"/files/{file_name}")
    if file_name == 'non_existent.file':
        assert response.status == 404
    elif file_name == 'empty.file':
        assert response.status == 200
        assert 'Content-Length' in response.headers
        assert response.headers['Content-Length'] == '0'