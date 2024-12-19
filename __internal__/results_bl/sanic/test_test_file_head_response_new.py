import os
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['non_existent.file', 'empty.file'])
async def test_head_response_for_non_existent_file(app: Sanic, file_name, static_file_directory):
    request, response = app.test_client.head(f"/files/{file_name}")
    assert response.status == 404

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
async def test_head_response_with_empty_file(app: Sanic, file_name, static_file_directory):
    empty_file_path = os.path.join(static_file_directory, 'empty.file')
    with open(empty_file_path, 'w') as f:
        pass
    request, response = app.test_client.head(f"/files/empty.file")
    assert response.status == 200
    assert response.headers['Content-Length'] == '0'
    os.remove(empty_file_path)

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
async def test_head_response_with_large_file(app: Sanic, file_name, static_file_directory):
    large_file_path = os.path.join(static_file_directory, 'large.file')
    with open(large_file_path, 'wb') as f:
        f.write(os.urandom(1024 * 1024))  # 1 MB file
    request, response = app.test_client.head(f"/files/large.file")
    assert response.status == 200
    assert 'Content-Length' in response.headers
    assert int(response.headers['Content-Length']) == 1024 * 1024
    os.remove(large_file_path)