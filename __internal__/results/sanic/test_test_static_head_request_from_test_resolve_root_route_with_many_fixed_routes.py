import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_head_request(app, file_name, static_file_directory):
    request, response = app.test_client.head("/testing.file")
    assert response.status == 200
    assert "method" in response.headers
    assert response.headers["method"] == "HEAD"
    assert response.body == b''

def test_head_request_with_invalid_path(app):
    request, response = app.test_client.head("/invalid.file")
    assert response.status == 404

def test_head_request_with_no_content(app):
    @app.route("/empty")
    async def empty_route(request):
        return text('', headers={'method': 'HEAD'})

    request, response = app.test_client.head("/empty")
    assert response.status == 200
    assert response.body == b''